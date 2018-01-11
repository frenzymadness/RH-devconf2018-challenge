#!/usr/bin/env python3
import sys
from subprocess import check_output, STDOUT, CalledProcessError
from itertools import cycle

PYTHON3 = '/usr/bin/python3'
PROFILER = ['/usr/bin/time', '-f', '"%e %M"']
TOKENIZER = [PYTHON3, '-m', 'tokenize']
TIMEOUT = 60
TIMEOUT_CMD = ['/usr/bin/timeout', str(TIMEOUT)]
DEBUG = True
checks = [
    ([1, 1, 3], True),
    ([1, 2, 3, 4, 5, 6], False),
    ([2, 3, 4, 5, 6, 7], True),
    ([3, 3, 3, 3, 6, 6], True),
    ([4, 4, 4, 4, 4, 4], True),
    ([1, 1, 1, 4], True),
    ([2, 3, 4], True),
    ([3, 4, 8, 8], True),
    ([3, 4, 6, 8], True),
    ([3, 5, 6, 8, 10], True),
    ([1, 1, 1], False)
]

performance_checks = [
    list(range(1, 11)),  # Small numbers, small, die, solution doesn't exists
    list(range(2, 12)),  # Small numbers, small die, solution exists
    list([x**3 for x in range(2, 12)]),  # Big numbers, small dice, solution exists
    list(range(2, 21)),  # Small numbers, big dice, solution exists
]


def run_script(script, arg):
    output = check_output([PYTHON3, script, arg])
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


def valid_solution(script):
    exit_code = 0

    for check in checks:
        enemy, better_exist = check
        player = run_script(script, ','.join([str(n) for n in enemy]))

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


def profile(script, arg):
    try:
        output = check_output(
            TIMEOUT_CMD + PROFILER + [PYTHON3, script, ','.join([str(x) for x in arg])],
            stderr=STDOUT)
    except CalledProcessError as e:
        time, memory = TIMEOUT * 2, None
    else:
        last_line = output.split(b'\n')[-2].replace(b'"', b'')
        time, memory = [float(x.strip()) for x in last_line.split()]
    return time, memory


def count_tokens(script):
    total = 0
    output = check_output(TOKENIZER + [script])
    lines = output.split(b'\n')
    for line in lines[:-1]:
        token = line.split()[1]
        if token not in [b'COMMENT', b'NL', b'NEWLINE']:
            total += 1
    
    return total


def main():
    script = sys.argv[1]

    valid, exit_code = valid_solution(script)

    if not valid:
        sys.exit(exit_code)

    total_time, total_mem = [], []

    checks_cycle = cycle(performance_checks)
    for _ in range(16):
        if DEBUG:
            print("Step {}, check {}".format(_, (_ % len(performance_checks) + 1)))
        check = next(checks_cycle)

        time, memory = profile(script, check)
        total_time.append(time)
        if memory is not None:
            total_mem.append(memory)

        if DEBUG:
            print('Time {}, memory {}'.format(time, memory))

    tokens = count_tokens(script)

    print('Average time is {:.4f}, average memory is {:.4f}, tokens {}'.format(
        sum(total_time)/len(total_time), sum(total_mem)/len(total_mem), tokens))


if __name__ == '__main__':
    main()
