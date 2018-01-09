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