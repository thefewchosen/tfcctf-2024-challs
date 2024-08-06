#include <stdio.h>
#include <stdlib.h>
#define NUM_CHUNKS 64

// Compile with:
// gcc main.c -o chall -pie -fstack-protector-all -Wl,-z,relro,-z,now

void print_menu() {
    printf("-------Menu-------\n");
    printf("1. Give me sum\n");
    printf("2. Take me sum\n");
    printf("3. Show me sum\n");
    printf("3. Don't give nun\n");
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
    if (size > 0x1000) {
        printf("Nope, too big\n");
        exit(0);
    } else {
        char *ptr = (char *)malloc(size + 1);
        printf("Data?\n");
        read(0, ptr, size);
        *(ptr + size) = '\0';
        chunk_ptrs[cnt_chunks++] = ptr;
        printf("Added at index %d\n", cnt_chunks - 1);
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

void print_memory() {
    unsigned int idx;
    printf("Which one?\n");
    printf("[+]> ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= NUM_CHUNKS) {
        printf("Invalid index\n");
        exit(0);
    } else {
        printf("Data: %s\n", chunk_ptrs[idx]);
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
                print_memory();
                break;
            case 4:
                printf("Get mogged!\n");
                exit(0);
            default:
                printf("Invalid choice\n");
        }
    }
}