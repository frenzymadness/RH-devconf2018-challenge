#!/usr/bin/env python3

import sys


def eval_prob(me, enemy):
    res = 0
    for m in me:
        for e in enemy:
            if m>e:
                res += 1
            if e>m:
                res -= 1
    return res


def find_combinations(count, total, min_val = 1):
    if count==1:
        yield [total]
    else:
        for i in range(min_val, total-min_val-count+2):
            if (total-i) >= (count-1) * i:
                for c in find_combinations(count-1, total-i, i):
                    yield [i] + c


def winning_die(enemy_die):
    for my_die in find_combinations(len(enemy_die), sum(enemy_die)):
        if eval_prob(my_die, enemy_die) > 0:
            return my_die
    return []


def main():
    numbers = [int(x.strip()) for x in sys.argv[1].split(',')]

    print(','.join([str(n) for n in winning_die(numbers)]))


if __name__ == '__main__':
    main()
