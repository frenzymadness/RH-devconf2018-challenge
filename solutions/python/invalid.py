#!/usr/bin/env python3

import itertools
import sys


def winning_die(enemy_die):
    faces = len(enemy_die)
    highest = min(max(enemy_die)+1, 18)
    summe = sum(enemy_die)

    for el in itertools.combinations_with_replacement(
            range(1, highest+1),
            faces):
        turn = list(el)
        if sum(turn) != summe:
            continue

        wins = 0
        ties = 0

        for i in range(faces):
            for j in range(faces):
                if enemy_die[i] < turn[j]:
                    wins += 1
                if enemy_die[i] == turn[j]:
                    ties += 1 

        try:            
            p = wins/(faces**2-ties)
            if p > 0.5:
                return turn

        except:
            pass

    return [1]


def main():
    numbers = [int(x.strip()) for x in sys.argv[1].split(',')]

    print(','.join([str(n) for n in winning_die(numbers)]))


if __name__ == '__main__':
    main()