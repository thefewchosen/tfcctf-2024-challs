#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include <stddef.h>

// ---------- BITWISE OPERATORS ----------
long xorFunction(long a, long b){
    long res = 0;
    for (long i = 63; i >= 0; i--)
    {
        bool b1 = a & (1 << i);
        bool b2 = b & (1 << i);
        bool xoredBit = (b1 & b2) ? 0 : (b1 | b2);
        res <<= 1;
        res |= xoredBit;
    }
    return res;
}

long shiftLeftFunction(long a, long num){
    long result = a;
    int i;
    for (i = 0; i < num; i++) {
        result *= 2;
    }
    return result;
}

long shiftRightFunction(long a, long num){
    long result = a;
    int i;
    for (i = 0; i < num; i++) {
        result /= 2;
    }
    return result;
}

long andFunction(long a, long b){
    long result = 0;
    long mask = 1;
    while (a > 0 && b > 0) {
        if (a % 2 == 1 && b % 2 == 1)
            result += mask;
        a /= 2;
        b /= 2;
        mask *= 2;
    }
    return result;
}

long orFunction(long a, long b){
    long result = 0;
    long mask = 1;
    while (a > 0 || b > 0) {
        if (a % 2 == 1 || b % 2 == 1)
            result += mask;
        a /= 2;
        b /= 2;
        mask *= 2;
    }
    return result;
}

long notFunction(long a){
    long result = 0;
    long mask = 1;
    long i;
    for (i = 0; i < sizeof(long) * 8; i++) {
        long bit = (a & mask) == 0 ? 1 : 0;
        result |= bit << i;
        mask <<= 1;
    }
    return result;
}

long negFunction(long a){
    return notFunction(a) + 1;
}

// ---------- Arithmetic operators ----------
long addFunction(long a, long b){
    while (b != 0)
    {
        unsigned long carry = a & b;  
        a = a ^ b; 
        b = carry << 1;
    }
    return a;
}

long subFunction(long a, long b){
    if (b == 0)
        return a;
    return subFunction(a ^ b, (~a & b) << 1);
}

long divFunction(long a, long b){
    if (a ^ a == a && b ^ b == b && a == b)
        return 0;
    long sign = ((a < 0) ^ (b < 0)) ? -1 : 1;
    a = abs(a);
    b = abs(b);

    long long quotient = 0;
    while (a >= b) {
        a -= b;
        ++quotient;
    }
    return quotient * sign;
}

long modFunction(long a, long b){
    if (b == 0) {
        return 0;
    }
    if (b < 0)
        b = -b;
    if (a < 0)
        a = -a;

    long i = 1;
    long product = 0;
    while (product <= a) {
        product = b * i;
        i++;
    }
    return a - (product - b);
}

long mulFunction(long a, long b){
    long result = 0;
    
    long sign = 1;
    if (b < 0) {
        sign = -1;
        b = -b;
    }
    
    while (b > 0) {
        result += a;
        b--;
    }
    
    if (sign == -1) {
        result = -result;
    }
    
    return result;
}

// ---------- Unary operators ----------
long incFunction(long a){
    long mask = 1;
    while ((a & mask) && mask) {
        a ^= mask;
        mask <<= 1;
    }
    if (mask)
        a ^= mask;
    return a;
}

long decFunction(long a){
    if (a == 1)
        return xorFunction(a, a);
    long test = ((a | (~a + 1)) >> 31) & 1;
    if (a == test)
        return !!a;
    long b = ~0;
    return (a & b) + ((a ^ b) >> 31);
}

// ---------- MISC ----------
long movFunction(long a, long b) {
    long x = (b ^ b);
    long y = (b | ~b);
    long z = (x + y);
    long w = (z >> 31);
    long v = ((b + w) & (~w));

    long result = (v & b) + (v ^ b);

    return result;
}

long exitFunction(long a){
    int exitSyscall = 0;
    void *heap_start = sbrk(0);
    ptrdiff_t difference = (char *)a - (char *)heap_start;
    if (difference < 0x21000) {
        int rdi = xorFunction(a, a);
        for (int i = 0; i < 60; i++)
            exitSyscall = incFunction(exitSyscall);
        
        syscall(exitSyscall, rdi);
    }
}

long syscallFunction(long lumaRegisters[]) {
    long m = xorFunction(0x10, 0x10);
    long j = addFunction(6, 2);

    for (long i = m; i < j; i = incFunction(i)) {
            lumaRegisters[i] = subFunction(i, i);
    }
}

long nopFunction(long a){
    return a;
}

int startGame = 0;
int gameLength = 0;

void checkWinFunction(long lumaRegisters[]) {
    if (lumaRegisters[0] == 1337 &&
    lumaRegisters[1] == 108 &&
    lumaRegisters[2] == 117 &&
    lumaRegisters[3] == 109 &&
    lumaRegisters[4] == 97)
    {
        FILE *file;
        char ch;

        file = fopen("./flag.txt", "r");
        if (file == NULL) {
            perror("Error opening file. Open a ticket.\n");
            exit(0);
        }

        while ((ch = fgetc(file)) != EOF) {
            putchar(ch);
        }

        fclose(file);
    }
}