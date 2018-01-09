# Red Hat Devconf 2018 challenge

## Task description

For this task, you're going to play a dice game, but first you must prepare
for an overwhelming victory. The game itself is very simple. Both players roll
a single die and whoever rolls highest scores a point. (On a tie, both players
must reroll until someone scores.)

These aren't standard dice however. Each player can put any positive number on
any side of the die as long as the number of sides match and the total of all
the chosen numbers are the same. For example, one player might use a six sided
die with the numbers [3, 3, 3, 3, 6, 6] while the other player uses a six sided
die with the numbers [4, 4, 4, 4, 4, 4]. The interesting part of this game is
that even with the same number of sides and the same total, different dice have
different chances of winning. Using the example die, the player with all 4's
will win 2/3 of the time.

To prepare for this game, you're investigating different ways of picking
the numbers. To do this, write a program that will take an opponent's die and
output some die which will win against it more than half the time. If no die
satisfies the task requirements, return an empty list.

## Input

Comma separated numbers representing opponent's die as a first command line
argument of your program.

For example:
```
$ <your_program> 3,3,3,3,6,6
```

## Output

Print your solution to `stdout` also as comma separated values. If solution
for given input doesn't exist, print empty string.

## Tests

Tests are implemented in `tests.py` and take your solution as a first command
line argument. In the output, each dot represents passing test. The last line
of the output contains profilling results.

For example:
```
$ ./tests.py brute_force.py 
.
.
.
.
.
.
.
.
.
.
.
.
Average time is 1.2984, average memory is 9391.6800
```

## Test results

```
for solution in brute_force.py generators.py longer_but_fast.py long.py short_magic.py; do echo -n "$solution - " && ./tests.py $solution | grep -v "^\." ; done
brute_force.py - Average time is 1.3192, average memory is 9388.6400, tokens 231
generators.py - Average time is 4.9748, average memory is 9388.3200, tokens 248
longer_but_fast.py - Average time is 0.0300, average memory is 9452.3200, tokens 317
long.py - Average time is 11.7912, average memory is 9478.5600, tokens 782
short_magic.py - Average time is 5.2232, average memory is 9381.6000, tokens 193
```
