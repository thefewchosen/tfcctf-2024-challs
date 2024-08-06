#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "./headers/registers.h"
#include "./headers/instructions.h"

#define MAX_BUFFER_SIZE 0x20
#define MAX_INSTRUCTION_SIZE 0x10

long pushFunction(long a);

char *operators[] = 
{
// Bitwise operators
"XZD", "STF", "QER", "LQE", "SQL",

// Arithmetic operators
"RALK", "MQZL", "LQDM", "SAMO", "XKA",

// Misc
"MISZ"
};

char *operatorsWith1Arg[] = {
// Bitwise operators
"NEAZ", "MINL",

// Unary operators
"OAN", "MAZ",

// Misc
"NO", "BRAILA"
};

size_t numOperators = sizeof(operators) / sizeof(operators[0]);
size_t numOperatorsWith1Arg = sizeof(operatorsWith1Arg) / sizeof(operatorsWith1Arg[0]);

// Index for the stack
int stackIndex = 0;

struct Data{
    char filename[11];
    long (*functions[12])(long, long);
    long (*functionsWith1Arg[6])(long);
} data = {
    .functions = {
    // Bitwise functions
    xorFunction, shiftLeftFunction, shiftRightFunction, andFunction, orFunction,

    // Arithmetic operators
    addFunction, subFunction, divFunction, modFunction, mulFunction,

    // Misc
    movFunction
    },
    .functionsWith1Arg = {
    // Bitwise functions
    notFunction, negFunction,

    // Unary functions
    incFunction, decFunction,

    // Misc
    nopFunction, exitFunction
    }
};

// For a harder reverse experience
int instructionUsed[12];
int instructionUsed2[6];

void checkIfOperatorExists(char opr[], int *index){
    int operatorFound = 0;
    for (int i = 0; i < numOperators; i++) {
        if (strcmp(opr, operators[i]) == 0) {
            operatorFound++;
            *index = i;
            break;
        }
    }
}

void checkIfOperatorWith1ArgExists(char opr[], int *index){
    int operatorFound = 0;
    for (int i = 0; i < numOperatorsWith1Arg; i++) {
        if (strcmp(opr, operatorsWith1Arg[i]) == 0) {
            operatorFound++;
            *index = i;
            break;
        }
    }
}

void checkIfSyscallWasCalled(char opr[], int *called){

    if (strcmp(opr, "FLG") == 0){
        *called = 1;
    }
}

int main(){

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    
    // Initialise registers with 0
    long lumaRegisters[] = {0, 0, 0, 0, 0, 0, 0, 0};
    initialiseRegisters(lumaRegisters);
    printf("-------------------------------------\n");

    // Get user instructions from stdin
    char *instructionsSentByUser = NULL;
    instructionsSentByUser = (char *)malloc(MAX_BUFFER_SIZE * sizeof(char));
    if (instructionsSentByUser == NULL){
        printf("Malloc allocation failed!");
        exit(0);
    }

    printf("Insert luma code: \n");
    while (1){
        fgets(instructionsSentByUser, MAX_BUFFER_SIZE - 1, stdin);
        instructionsSentByUser[strlen(instructionsSentByUser) - 1] = '\0';
        if (strlen(instructionsSentByUser) == 0){
            printf("LUMA_ERROR (0): Trying to execute nothing!\n");
            exit(0);
        }

        // Extract instruction with arguments (if they exist)
        char instruction[MAX_BUFFER_SIZE];
        char arg1[MAX_BUFFER_SIZE] = {'\0'}, arg2[MAX_BUFFER_SIZE] = {'\0'};
        char *token = strtok(instructionsSentByUser, " \n");
        strncpy(instruction, token, MAX_INSTRUCTION_SIZE);
        
        // Operation does not exit? -> exit
        // It does? -> save the index of it to execute later
        int index = -1, indexFunctionsWith1Arg = -1, syscall = -1, cmp = -1;
        int indexArg1 = -1, indexArg2 = -1;
        checkIfOperatorExists(instruction, &index);
        checkIfOperatorWith1ArgExists(instruction, &indexFunctionsWith1Arg);
        checkIfSyscallWasCalled(instruction, &syscall);
        if (index == -1 && indexFunctionsWith1Arg == -1 && syscall == -1) {
            printf("LUMA_ERROR (1): Invalid instruction name!\n");
            exit(0);
        }
        token = strtok(NULL, ",");
        if (token != NULL) {
            strncpy(arg1, token, 3);
            if (arg1[0] == ' ')
                memmove(arg1, arg1 + 1, strlen(arg1));
            checkIfRegisterExists(arg1, &indexArg1);
        }   

        token = strtok(NULL, "\n");
        if (token != NULL) {
            strncpy(arg2, token, 3);
            if (arg2[0] == ' ')
                memmove(arg2, arg2 + 1, strlen(arg2));
            checkIfRegisterExists(arg2, &indexArg2);
        }

        // We found a function that only requires 1 argument, are there 2? or vice versa
        if  ( (indexFunctionsWith1Arg != -1 && (indexArg2 != -1 || indexArg1 == -1)) || 
              (index != -1 && (indexArg1 == -1 || indexArg2 == -1)) || 
              (syscall != -1 && (indexArg1 != -1 || indexArg2 != -1)) 
            )
        {
            printf("LUMA_ERROR (3): Invalid registers for this type of instruction!\n");
            exit(0);
        }

        // Make sure the instruction hasn't been used too much
        for (int i = 0; i < numOperators; i++)
            if (instructionUsed[i] > 10){
                printf("LUMA_ERROR (4): Due to efficiency reasons, we won't let you use the same instruction too much!\n");
                exit(0);
            }
        
        for (int i = 0; i < numOperatorsWith1Arg; i++)
            if (instructionUsed2[i] > 10){
                printf("LUMA_ERROR (4): Due to efficiency reasons, we won't let you use the same instruction too much!\n");
                exit(0);
            }

        // Execute the instruction
        if (syscall == -1){
            if (indexFunctionsWith1Arg == -1){
                instructionUsed[index]++;
                lumaRegisters[indexArg1] = data.functions[index](lumaRegisters[indexArg1], lumaRegisters[indexArg2]);
            }else{
                instructionUsed2[indexFunctionsWith1Arg]++;
                lumaRegisters[indexArg1] = data.functionsWith1Arg[indexFunctionsWith1Arg](lumaRegisters[indexArg1]);
            }
        }
        else
            checkWinFunction(lumaRegisters);
    }

    free(instructionsSentByUser);
    return 0;
}