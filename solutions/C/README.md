# Implementing the challenge in C

## Prerequisites

You're going to need an implementation clang. If you're using Linux, just install the 
package. If you're using Windows, go fish.

## Submitting your solution

You must submit your solution in the form of Java source code. This source code must be placed in one and only one file
with a name of your choosing. Your solution must compile using the following command, without any extra dependencies:

    $ clang YourSolutionFile.c -o solution

Your solution must include the standard C `main method`, that is a method with the following signature:

    int main(int argc, char *argv[])

We will use this method as the entry point to your submitted solution, using a command such as this:

    $ ./solution 1,2,3,4,5,6
    
Your solution must not print anything to the standard input or output, other than the final computation result.

