#!/usr/bin/env python3

import sys


def winning_die(enemy_die):
    len_die = len(enemy_die)
    sum_die = sum(enemy_die)
    max_die = max(enemy_die)
    # i_lst = list(range(1, (max_die + 1) + 1))
    i_lst = range(1, (max_die + 1) + 1)
    c_lst = [sum(d < i for d in enemy_die) - sum(d > i for d in enemy_die) for i in i_lst]

    def inner(v_min, v_max):
        assert len(v_min) == len(v_max)
        f = True
        while f:
            f = False
            len_min = 0
            len_max = 0
            for lo, hi in zip(v_min, v_max):
                if lo > hi:
                    return
                len_min += lo
                len_max += hi
            if len_min > len_die or len_max < len_die:
                return
            for j in range(len(v_min)):
                lo = v_min[j]
                hi = v_max[j]
                if len_min + (hi - lo) > len_die:
                    f = True
                    v_max[j] = lo + (len_die - len_min)
                if len_max - (hi - lo) < len_die:
                    f = True
                    v_min[j] = hi - (len_max - len_die)
            sum_min = 0
            sum_max = 0
            for i, lo, hi in zip(i_lst, v_min, v_max):
                if lo > hi:
                    return
                sum_min += i * lo
                sum_max += i * hi
            if sum_min > sum_die or sum_max < sum_die:
                return
            for j in range(len(v_min)):
                i = i_lst[j]
                lo = v_min[j]
                hi = v_max[j]
                if sum_min + i * (hi - lo) > sum_die:
                    f = True
                    v_max[j] = lo + (sum_die - sum_min) // i
                if sum_max - (hi - lo) < sum_die:
                    f = True
                    v_min[j] = hi - (sum_max - sum_die) // i
            score_min = 0
            score_max = 0
            for c, lo, hi in zip(c_lst, v_min, v_max):
                if lo > hi:
                    return
                if c > 0:
                    score_min += c * lo
                    score_max += c * hi
                elif c < 0:
                    score_min += c * hi
                    score_max += c * lo
            if score_max <= 0:
                return
            for j in range(len(v_min)):
                c = c_lst[j]
                lo = v_min[j]
                hi = v_max[j]
                if score_max - abs(c) * (hi - lo) <= 0:
                    f = True
                    if c > 0:
                        v_min[j] = hi - (score_max - 1) // c
                    elif c < 0:
                        v_max[j] = lo + (score_max - 1) // (-c)
        for j, (lo, hi) in enumerate(zip(v_min, v_max)):
            if lo > hi:
                return
            if lo < hi:
                for v_cand in range(lo, hi + 1):
                    v_min_copy = v_min[:]
                    v_max_copy = v_max[:]
                    v_min_copy[j] = v_cand
                    v_max_copy[j] = v_cand
                    for sol in inner(v_min_copy, v_max_copy):
                        yield sol
                return
        sol = []
        for i, v in zip(i_lst, v_min):
            for __ in range(v):
                sol.append(i)
        yield sol

    res = list(zip((0,), inner([0 for i in i_lst], [len_die for i in i_lst])))

    return res[0][1] if res else []


def main():
    numbers = [int(x.strip()) for x in sys.argv[1].split(',')]

    print(','.join([str(n) for n in winning_die(numbers)]))


if __name__ == '__main__':
    main()
