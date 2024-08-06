#include <stdio.h>
#include <stdlib.h>
#define NUM_CHUNKS 64

void print_menu() {
    printf("-------Menu-------\n");
    printf("1. Allocate memory\n");
    printf("2. Free memory\n");
    printf("3. Give up\n");
    printf("------------------\n");
    printf("[+]> ");
}

int cnt_chunks = 0;
char *chunk_ptrs[NUM_CHUNKS];

void allocate_memory() {
    if (cnt_chunks >= NUM_CHUNKS) {
        printf("No more memory available\n");
        exit(0);
    }

    unsigned int size;
    printf("How much?\n");
    printf("[+]> ");
    scanf("%d", &size);
    if (size > 0x70) {
        printf("Nope, too big\n");
        exit(0);
    } else {
        char *ptr = (char *)malloc(size + 1);
        printf("Data?\n");
        read(0, ptr, size);
        *(ptr + size) = '\0';
        chunk_ptrs[cnt_chunks++] = ptr;
        printf("Job done!\n");
    }
}

void free_memory() {
    unsigned int idx;
    printf("Which one?\n");
    printf("[+]> ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= NUM_CHUNKS) {
        printf("Invalid index\n");
        exit(0);
    } else {
        free(chunk_ptrs[idx]);
        printf("Job done!\n");
    }
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    for (int i = 0; i < NUM_CHUNKS; i++) {
        chunk_ptrs[i] = NULL;
    }

    int choice;
    while (1) {
        print_menu();
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                allocate_memory();
                break;
            case 2:
                free_memory();
                break;
            case 3:
                printf("Is that all you got? Bye!\n");
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }
}