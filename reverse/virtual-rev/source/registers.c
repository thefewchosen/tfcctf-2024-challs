#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "./headers/registers.h"


const char *registerNames[] = {"l0", "l1", "l2", "l3", "l4", "l5", "lax", "lip"};
size_t numRegisters = sizeof(registerNames) / sizeof(registerNames[0]);

void initialiseRegisters(long *lumaRegisters){
    printf("Registers initialised: \n");
    for (int i = 0; i < numRegisters - 1; i++)
        printf("(%s) = 0x%016lx\n", registerNames[i], lumaRegisters[i]);

    lumaRegisters[7] = (long int)__builtin_return_address(0);
    printf("(lip) = 0x%016lx\n", lumaRegisters[7]);
}

// Register does not exist? -> exit
// Register exists? -> save index of it so we know what function arguments we execute.
void checkIfRegisterExists(char reg[], int *index){
    int registerFound = 0;
    for (int i = 0; i < numRegisters; i++) {
        if (strcmp(reg, registerNames[i]) == 0) {
            registerFound++;  
            *index = i;
            break;
        }
    }

    if (registerFound == 0) {
        printf("LUMA_ERROR (2): Register name is invalid!\n");
        exit(0);
    }
}