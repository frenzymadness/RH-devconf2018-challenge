/* mathy.c
 *
 * Copyright (C) 2018 Red Hat, Inc.
 *
 * Authors: Jiri Vymazal <jvymazal@redhat.com>
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

	int avg = sum/sides;
	int rem = sum%sides;
	int above = 0;
	int below = 0;
	int ones = 0;
	int max = 0;
	int min = opponent[0];
	int min_above = 0;

	for (int i = 0; i < sides; i++)
	{
		if (opponent[i] == 1)
		{
			ones++;
		}
		if (opponent[i] > max)
		{
			max = opponent[i];
		}
		if (opponent[i] < min)
		{
			min = opponent[i];
		}
		if (opponent[i] > avg)
		{
			if (!min_above || min_above > opponent[i])
			{
				min_above = opponent[i];
			}
			above++;
			continue;
		}
		if (opponent[i] < avg || rem)
		{
			below++;
		}
	}
	if (sum == mid || max <= 2)
	{
		printf("\n");
		return EXIT_SUCCESS;
	}

	int pool = sum;

	if (above <= below)
	{
		for (int i = 0; i < sides; i++)
		{
			int top = 1 + (sum-mid)/sides;
			int low = 1;
			if (!rem && (min != max))
			{
				top--;
			}
			else if (avg == below && min_above > avg+top)
			{
				top = min_above - avg;
				low = min+1;
			}
			if ((pool - (avg+top)) >= (sides - i - 1)*low)
			{
				better[i] = avg+top;
				pool -= better[i];
			}
			else if (sides > i+1)
			{
				if ((pool - (min+1)) >= (sides - i - 1))
				{
					better[i] = min+1;
					pool -= better[i];
				}
				else
				{
					better[i] = 1;
					pool -= better[i];
				}
			}
			else
			{
				better[i] = pool;
			}
		}
		print_dice(better, sides);
		return EXIT_SUCCESS;
	}
	if (above > below)
	{
		if(ones)
		{
			for (int i = 0; i < sides; i++)
			{
				if ((pool - (max+1)) > (sides - i))
				{
					better[i] = max+1;
					pool -= better[i];
				}
				else if (pool > (sides - i))
				{
					better[i] = pool - (sides - i - 1);
					pool -= better[i];
				}
				else
				{
					better[i] = 1;
					pool -= better[i];
				}
			}
		}
		else
		{
			for (int i = 0; i < sides; i++)
			{
				if ((pool - (max+1)) > (sides - i - 1))
				{
					better[i] = max+1;
					pool -= better[i];
				}
				else if (sides > i+1)
				{
					better[i] = 1;
					pool -= better[i];
				}
				else
				{
					better[i] = pool;
				}
			}
		}
		print_dice(better, sides);
		return EXIT_SUCCESS;
	}

	//we should never get here unless something really wrong happened
	fprintf(stderr, "dice-calc: undefined internal ERROR, please report to <jvymazal@redhat.com>, thanks!\n"); 
	return EXIT_FAILURE;
}
