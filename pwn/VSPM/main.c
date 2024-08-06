#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#define MAX_PTRS 10
#define NAME_LEN 32

typedef struct {
    char* pointer;
    char name[NAME_LEN];
} Credential;

Credential ptrs[MAX_PTRS] = {NULL};

void win(){
    system("/bin/sh");
}

void setup(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void savePassword(){

    int i;
    for (i = 0; i < 10; i++){
        if (ptrs[i].pointer == NULL){
            break;
        }
    }

    if (i == MAX_PTRS) {
        printf("No more space to save passwords.\n");
        exit(0);
    }

    printf("\nSelect length: ");
    int len = 0;
    scanf("%d", &len);
    getchar();
    if (len < 0 || len > 0x80-8){
        printf("Sorry, not enough resources!\n");
        exit(0);
    }
    char caca[40] = {0};
    ptrs[i].pointer = (char *)malloc(len * sizeof(char));
    printf("Enter credentials: ");
    
    read(0, ptrs[i].pointer, len+1);

    printf("Name of the credentials: ");
    read(0, ptrs[i].name, NAME_LEN+1);
}

void listPasswords(){
    for (int i = 0; i < 10; i++){
        if (ptrs[i].pointer != NULL){
            printf("%d. %.*s --> %s", i, NAME_LEN, ptrs[i].name, ptrs[i].pointer);
        }
    }
}

void deletePassword(){
    int index = 0;
    printf("Select index: ");
    scanf("%d", &index);
    getchar();

    if (ptrs[index].pointer == NULL){
        printf("You can't delete a non-existent password.\n");
        exit(0);
    }

    free(ptrs[index].pointer);
    ptrs[index].pointer = NULL;
    memset(ptrs[index].name, 0, 32);
}

void exitFunction(){

    printf("Goodbye! See you soon.\n");
    exit(0);
}


int main(){

    setup();

    printf("Welcome to the Very Secure Password Manager!\n");
    printf("--------------------------------------------\n\n");
    printf("1. Save new password\n");
    printf("2. Check my passwords\n");
    printf("3. Delete credentials\n");
    printf("4. Exit\n");

    while(1){
        
        int choice = 0;
        printf("Input: ");
        scanf("%d", &choice);
        getchar();
        if (choice < 1 || choice > 4){
            printf("Not a valid choice :(\n");
            exit(0);
        }

        switch(choice) {
        case 1:
            savePassword();
            break;
        case 2:
            listPasswords();
            break;
        case 3:
            deletePassword();
            break;
        case 4:
            exitFunction();
            break;
        }
    }

    return 0;
}