#!/usr/bin/env python3

import sys


def winning_die(enemy_die):
    dim = len(enemy_die)
    total = sum(enemy_die)
    win = [0 for _ in range(total + 1)]
    for i in range(1, total + 1):
        for j in enemy_die:
            win[i] += (i > j) - (j > i)
    subanswers = [[(0, 0) for tot in range(total + 1)] for die in range(dim + 1)]

    for num_die in range(0, dim):
        for subsum in range(num_die + 1, total + 1):
            possibilities = []
            for last in range(1, subsum - num_die + 1):
                poss = (win[last] + subanswers[num_die][subsum - last][0], last)
                possibilities.append(poss)
            subanswers[num_die + 1][subsum] = max(possibilities)
    ans = []
    if subanswers[dim][total][0] > 0:
        cur = total
        for i in range(dim):
            side = subanswers[dim - i][cur][1]
            ans.append(side)
            cur -= side
    return ans


def main():
    numbers = [int(x.strip()) for x in sys.argv[1].split(',')]

    print(','.join([str(n) for n in winning_die(numbers)]))


if __name__ == '__main__':
    main()
