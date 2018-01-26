#!/usr/bin/python3 -u
import sys
from subprocess import call, check_output, STDOUT, CalledProcessError
from itertools import cycle
import re
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import json


API_TOKEN = 'G$^ubX&vGaoYCglKRcfJ7QOXHgj~~W2&'
BASE_URL = 'https://devconf.fedoralovespython.org'
API = BASE_URL + '/api/' + API_TOKEN
HEADERS = {'User-Agent': 'Mozilla/5.0'}
COMPILERS = {
    'java': ['/usr/bin/javac'],
    'c': ['clang', '-o', 'candidate']
}
RUNNERS = {
    'py': ['/usr/bin/python3'],
    'java': ['java', '-Xms32m', '-Xmx32m'],
    'c': []
}
PROFILER = ['/usr/bin/time', '-f', '"%e %M"']
TOKENIZERS = {
    'py': RUNNERS['py'] + ['-m', 'tokenize'],
    'java': ['java', '-jar', 'java-tokenizer.jar'],
    'c': ['tokenize']
}
TIMEOUT = 60
TIMEOUT_CMD = ['/usr/bin/timeout', str(TIMEOUT)]
DEBUG = True
checks = [
    ([1, 1, 3], True),
    ([1, 2, 3, 4, 5, 6], False),
    ([2, 3, 4, 5, 6, 7], True),
    ([3, 3, 3, 3, 6, 6], True),
    ([4, 4, 4, 4, 4, 4], True),
    ([7, 7, 6, 1, 1, 1, 1], True),
    ([7, 7, 6, 1, 1, 1], True),
    ([1, 1, 1, 4], True),
    ([2, 3, 4], True),
    ([3, 4, 8, 8], True),
    ([3, 4, 6, 8], True),
    ([3, 5, 6, 8, 10], True),
    ([1, 1, 1], False)
]

performance_checks_others = [
    list(range(1, 11)),  # Small numbers, small dice, solution doesn't exists
    list(range(1, 15)),  # Small numbers, big dice, solution doesn't exists
    list(range(2, 12)),  # Small numbers, small dice, solution exists
    list([x**3 for x in range(2, 12)]),  # Big numbers, small dice, solution exists
    list(range(2, 21)),  # Small numbers, big dice, solution exists
    list([x**3 for x in range(2, 14)]),  # Big numbers, small dice, solution exists
]

performance_checks_for_c = [
    list(range(1, 201)),   # Small numbers, big dice, solution doesn't exists
    list(range(2, 201)),   # Small numbers, big dice, solution exists
    list([x**3 for x in range(2, 51)]),  # Big numbers, small dice, solution exists
    list([x**5 for x in range(2, 25)]),  # Big numbers, small dice, solution exists
]


def run_script(script, extension, arg):
    output = check_output(RUNNERS[extension] + [script, arg])
    output = output.strip()
    if output == b"":
        return None
    else:
        numbers = [int(n.strip()) for n in output.split(b',')]

    return numbers


def is_players_die_better(player, enemy):
    total_wins = 0
    for p in player:
        for e in enemy:
            if p > e:
                total_wins += 1
            elif p < e:
                total_wins -= 1
    return total_wins > 0


def valid_solution(script, extension):
    exit_code = 0

    for check in checks:
        enemy, better_exist = check
        player = run_script(script, extension, ','.join([str(n) for n in enemy]))

        if not better_exist:
            if player is None:
                print('.')
            else:
                print('You cannot beat this die. Enemy:{} vs Player:{}'.format(enemy, player))
                exit_code += 1
        else:
            if player is None:
                print('You can beat this one. Enemy:{} vs Player:{}'.format(enemy, player))
                exit_code += 1
                continue
            if not min(player) > 0:
                print('You cannot use zeros. Enemy:{} vs Player:{}'.format(enemy, player))
                exit_code += 1
                continue
            if sum(player) != sum(enemy):
                print("Player's die has different sum. Enemy:{} vs Player:{}".format(enemy, player))
                exit_code += 1
                continue
            if len(player) != len(enemy):
                print("Player's die has different length. Enemy:{} vs Player:{}".format(enemy, player))
                exit_code += 1
                continue
            if is_players_die_better(player, enemy):
                print('.')
            else:
                print("Player's die is not better. Enemy:{} vs Player:{}".format(enemy, player))
                exit_code += 1

    if exit_code > 0:
        return False, exit_code
    else:
        return True, exit_code


def profile(script, extension, arg):
    try:
        output = check_output(
            TIMEOUT_CMD + PROFILER + RUNNERS[extension] + [script, ','.join([str(x) for x in arg])],
            stderr=STDOUT)
    except CalledProcessError as e:
        time, memory = TIMEOUT * 2, None
    else:
        last_line = output.split(b'\n')[-2].replace(b'"', b'')
        time, memory = [float(x.strip()) for x in last_line.split()]
    return time, memory


def count_tokens(script, extension):
    total = 0
    output = check_output(TOKENIZERS[extension] + [script])
    if extension == 'py':
        lines = output.split(b'\n')
        for line in lines[:-1]:
            token = line.split()[1]
            if token not in [b'COMMENT', b'NL', b'NEWLINE']:
                total += 1
    if extension == 'c' or extension == 'java':
        result = re.findall('\d+', output.decode('utf-8'))
        return int(result[0])

    return total


def clean():
    call(['git', 'clean', '-fd'])


def fetch_unrated_files():
    # Get list of unrated files
    url = API + '/unrated'
    req = Request(url, headers=HEADERS)
    files = urlopen(req).read().decode('utf-8').strip().split('\n')

    if not files or len(files) == 1 and '' in files:
        print('Nothing to do.')
        sys.exit(0)

    # Download each unrated file
    for file_name in files:
        file_url = BASE_URL + '/file/' + file_name
        req = Request(file_url, headers=HEADERS)

        # Use file original name
        original_file_name = file_name.split('___')[-1]

        with open(original_file_name, 'wb') as file:
            file.write(urlopen(req).read())

        yield file_name, original_file_name


def prepare_solution(file_name):
    script = file_name
    source_code = script

    extension = source_code.split('.')[-1]
    if extension not in ['java', 'py', 'c']:
        print('Unknown solution language!')
        sys.exit(1)

    if extension in COMPILERS.keys():
        call(COMPILERS[extension] + [source_code])

    if extension == 'c':
        script = './candidate'
    elif extension == 'java':
        script = source_code.rstrip('.java')

    return source_code, script, extension


def mark_solution_invalid(file_name):
    url = API + '/invalid/' + file_name
    req = Request(url, headers=HEADERS)
    try:
        json_response = urlopen(req).read()
    except:
        print('Error during API call!')
        print('JSON response: {}'.format(json.loads(json_response)))


def rate_solution(file_name, time, memory, tokens, timeouted=False):
    url = API + '/rate/'
    data = {
        'filename': file_name,
        'time': round(time, 3),
        'memory': round(memory, 3),
        'tokens': tokens
    }
    if timeouted:
        data['timeouted'] = True

    req = Request(url, data=urlencode(data).encode(), headers=HEADERS)
    try:
        json_response = urlopen(req).read()
    except:
        print('Error during API call!')
        print('JSON response: {}'.format(json.loads(json_response)))


def main():

    for file_name, original_file_name in fetch_unrated_files():

        if DEBUG:
            print('Testing {}'.format(file_name))

        # Prepare solution file, compile etc.
        source_code, script, extension = prepare_solution(original_file_name)

        # Check validity
        valid, exit_code = valid_solution(script, extension)

        if not valid:
            if DEBUG:
                print('Solution is not valid. Skipping performance checks')
            mark_solution_invalid(file_name)
            clean()
            continue

        # Use harder performance checks for solutions in C
        if extension == 'c':
            performance_checks = performance_checks_for_c
        else:
            performance_checks = performance_checks_others

        # Do performance checks
        total_time, total_mem = [], []

        checks_cycle = cycle(performance_checks)
        for _ in range(16):
            if DEBUG:
                print("Step {}, check {}".format(_, (_ % len(performance_checks) + 1)))
            check = next(checks_cycle)

            time, memory = profile(script, extension, check)

            if time == TIMEOUT * 2:
                if DEBUG:
                    print('Solution timeouted with {}'.format(check))
                rate_solution(file_name, 0, 0, 0, timeouted=True)
                clean()
                sys.exit(1)

            total_time.append(time)
            if memory is not None:
                total_mem.append(memory)

            if DEBUG:
                print('Time {}, memory {}'.format(time, memory))

        # Count tokens in source code
        if extension in TOKENIZERS.keys():
            tokens = count_tokens(source_code, extension)
        else:
            tokens = None

        # Calculate averages and call API with results
        avg_time = sum(total_time)/len(total_time)
        avg_mem = sum(total_mem)/len(total_mem)

        if DEBUG:
            print('Average time is {:.4f}, average memory is {:.4f}, tokens {}'.format(
                avg_time, avg_mem, tokens))

        rate_solution(file_name, avg_time, avg_mem, tokens)

        clean()


if __name__ == '__main__':
    main()
