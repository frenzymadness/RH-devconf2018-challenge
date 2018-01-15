# Implementing the challenge in Java

## Prerequisites

You're going to need an implementation of Java SE 9, preferably OpenJDK 9. If you're using Linux, just install the 
package. If you're using Windows, go fish.

## Submitting your solution

You must submit your solution in the form of Java source code. This source code must be placed in one and only one file
with a name of your choosing. Your solution must compile using the following command, without any extra dependencies:

    $ javac YourSolutionFile.java

Your solution must include the standard Java `main method`, that is a method with the following signature:

    public static void main(final String... args)

We will use this method as the entry point to your submitted solution, using a command such as this:

    $ java YourSolutionFile 1,2,3,4,5,6
    
Your solution must not print anything to the standard input or output, other than the final computation result.

## Specifics of the JVM we're using

To run your code, we will be using the following JRE (FIXME replace with the actual Java you'll be using):

    openjdk version "9.0.1"
    OpenJDK Runtime Environment (build 9.0.1+11)
    OpenJDK 64-Bit Server VM (build 9.0.1+11, mixed mode)`
    
Your code will be run on `Intel Core i7-6600U CPU @ 2.60GHz` with 20GB RAM and an SSD drive, running Fedora 27. 
(FIXME replace with the actual configuration). We will be limiting the memory allocation pool to 32 megabytes.

The final command we will use to run your submission will therefore be:

    $ java -Xms32m -Xmx32m YourSolutionFile 1,2,3,4,5,6
  
We are aware of the fact that this JVM configuration may make several non-deterministic performance optimizations which 
may give unfair advantage to different solutions running in different JVM instances. To offset this, we will be 
executing each submission multiple times and the resulting score will be based on an average of the individual execution 
times.
