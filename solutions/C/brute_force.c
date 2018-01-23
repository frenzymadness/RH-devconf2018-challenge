/* brute_force.c
 *
 * Copyright (C) 2018 Red Hat, Inc.
 *
 * Authors: Jiri Vymazal <jvymazal@redhat.com>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

bool test(int op[], int cand[], int sides)
{
	int score = 0;
	for (int i = 0; i < sides; i++)
	{
		for (int j = 0; j < sides; j++)
		{
			if (cand[i] > op[j])
			{
				score++;
			}
			else if (cand[i] < op[j])
			{
				score--;
			}
		}
	}
	if (score > 0)
	{
		return true;
	}
	else 
	{
		return false;
	}
}

void print_dice(int dice[], int sides)
{
	for (int i = 0; i < sides; i++)
	{
		if (i)
		{
			printf(",");
		}
		printf("%d", dice[i]);
	}
	printf("\n");
}

void process_side(int *sides, int *side_len, int *max_side_len)
{
	if (*side_len == 0)
	{
		fprintf(stderr, "dice-calc: input dice contains empty side!\n");
		exit(EXIT_FAILURE);
	}
	(*sides)++;
	if (*side_len > *max_side_len)
	{
		*max_side_len = *side_len;
	}
	*side_len = 0;
}

int main(int argc, char *argv[])
{
	if (argc != 2)
	{
		fprintf(stderr, "dice-calc: invalid number of arguments given, expecting exactly 1\n");
		return EXIT_FAILURE;
	}

	//first pass to determine number of sides we are playing with (and validate input)
	int n = 0;
	int sides = 0;
	int max_side_len = 0;
	int side_len = 0;
	while (argv[1][n])
	{
		switch (argv[1][n])
		{
			case '0':
			case '1':
			case '2':
			case '3':
			case '4':
			case '5':
			case '6':
			case '7':
			case '8':
			case '9':
				side_len++;
				break;
			case ',':
				process_side(&sides, &side_len, &max_side_len);
				break;
			default:
				fprintf(stderr, "dice-calc: invalid character in input dice:%c\n", argv[1][n]);
				return EXIT_FAILURE;
		}
		n++;
	}
	process_side(&sides, &side_len, &max_side_len);
	if (sides < 3)
	{
		printf("\n");
		return EXIT_SUCCESS;
	}

	int opponent[sides];
	int curr_side = 0;
	int better[sides];
	int sum = 0;
	int mid = 1;

	//second pass for conversion to int array
	char str[max_side_len+1];
	n = 0;
	while (argv[1][n])
	{
		if (argv[1][n] == ',')
		{
			str[side_len] = '\0';
			opponent[curr_side] = atoi(str);
			if (opponent[curr_side] < 1) //either zero side entered or some atoi error
			{
				fprintf(stderr, "dice-calc: non-positive or invalid side in input!\n");
				return EXIT_FAILURE;
			}
			sum += opponent[curr_side];
			side_len = 0;
			curr_side++;
			mid += curr_side+1;
		}
		else	//number
		{
			str[side_len] = argv[1][n];
			side_len++;
		}
		n++;
	}
	str[side_len] = '\0';
	opponent[curr_side] = atoi(str);
	if (opponent[curr_side] < 1) //either zero side entered or some atoi error
	{
		fprintf(stderr, "dice-calc: non-positive or invalid side in input!\n");
		return EXIT_FAILURE;
	}
	sum += opponent[curr_side];
	int max = 0;

	for (int i = 0; i < sides; i++)
	{
		if (opponent[i] > max)
		{
			max = opponent[i];
		}
	}
	if (sum == mid || max <= 2)
	{
		printf("\n");
		return EXIT_SUCCESS;
	}

	bool first_run = true;
	int pool = 0;
	int next = 0;
	while(1)
	{
		pool = sum;
		if (first_run)
		{
			first_run = false;
			for (int i = 0; i < sides-1; i++)
			{
				better[i] = 1;
				pool -= better[i];
			}
			better[sides-1] = pool;
		}
		else
		{
			better[next]++;
			next++;
			if (next == sides-1)
			{
				next = 0;
			}
			better[sides-1]--;
		}
		if (test(opponent, better, sides))
		{
			print_dice(better, sides);
			return EXIT_SUCCESS;
		}
	}
	
	//we should never get here
	return EXIT_FAILURE;
}
