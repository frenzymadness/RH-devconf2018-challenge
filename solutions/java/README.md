# Implementing the challenge in Java

## Prerequisites

You're going to need an implementation of Java SE 9, preferably OpenJDK 9. If you're using Linux, just install the 
package. If you're using Windows, go fish.

## Submitting your solution

You must submit your solution in the form of Java source code. This source code must be placed in one and only one file
with a name of your choosing. Your solution must compile using the following command, without any extra dependencies:

    [lpetrovi@sagan src]$ javac YourSolutionFile.java

Your solution must include the standard Java `main method`, that is a method with the following signature:

    public static void main(final String... args)

We will use this method as the entry point to your submitted solution, using a command such as this:

    [lpetrovi@sagan src]$ java YourSolutionFile 1,2,3,4,5,6
    
Your solution must not print anything to the standard input or output, other than the final computation result.

## Specifics of the JVM we're using

To run your code, we will be using the following JRE (FIXME replace with the actual Java you'll be using):

    [lpetrovi@sagan src]$ java -version
    openjdk version "9.0.1"
    OpenJDK Runtime Environment (build 9.0.1+11)
    OpenJDK 64-Bit Server VM (build 9.0.1+11, mixed mode)`
    
Your code will be run on `Intel Core i7-6600U CPU @ 2.60GHz` with 20GB RAM and an SSD drive, running Fedora 27. 
(FIXME replace with the actual configuration.
    
In the absence of sophisticated performance measurements, we will be disabling JVM performance optimizations to make the
performance of your code slightly more deterministic. We will also be limiting the memory allocation pool to 32 megabytes.

The final command we will use to run your submission will therefore be:

    [lpetrovi@sagan src]$ java -Xms32m -Xmx32m -Xint YourSolutionFile 1,2,3,4,5,6
  