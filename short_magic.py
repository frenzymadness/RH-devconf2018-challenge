#!/usr/bin/env python3

import sys


def winning_die(enemy):
    def explore(rlen, rlist, rsum, rmin):
        if rlen:
            for one in range(rmin, 1 + rsum // rlen) if rlen > 1 else [rsum]:
                yield from explore(rlen - 1, rlist + [one], rsum - one, one)
        elif sum((p > e)-(p < e) for p in rlist for e in enemy) > 0:
            yield rlist
    return next(explore(len(enemy), [], sum(enemy), 1), [])


def main():
    numbers = [int(x.strip()) for x in sys.argv[1].split(',')]

    print(','.join([str(n) for n in winning_die(numbers)]))


if __name__ == '__main__':
    main()
