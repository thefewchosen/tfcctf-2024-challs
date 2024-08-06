#ifndef INSTRUCTIONS_H
#define INSTRUCTIONS_H

#include <stdio.h>

// Bitwise functions
long xorFunction(long a, long b);
long addFunction(long a, long b);
long shiftLeftFunction(long a, long num);
long shiftRightFunction(long a, long num);
long orFunction(long a, long b);
long notFunction(long a);
long negFunction(long a);

// Arithmetic functions
long andFunction(long a, long b);
long subFunction(long a, long b);
long divFunction(long a, long b);
long modFunction(long a, long b);
long mulFunction(long a, long b);
long movQwordFunction(long a, long b);

// Unary functions
long incFunction(long a);
long decFunction(long a);

// Misc
long nopFunction(long a);
long movFunction(long a, long b);
long exitFunction(long a);

// Syscall
void syscallFunction(long a[]);
long cmpFunction(long a, long b, char* filename);

#endif
