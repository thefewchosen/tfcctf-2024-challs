#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAX_ENTRIES 256

void banner() {
    printf("guava gius is not something you can just indulge in\n");
    printf("guava gius guavocado is a lifestyle\n");
    printf("guava is the single most important piece of guavocado\n");
    printf("that you are supposed to buava and muava guava\n");
    printf("muava mus or muava guava? simi gus\n");
    printf("\n");
}

void menu() {
    printf("1. guava\n");
    printf("2. gius\n");
    printf("3. guavocado\n");
    printf("*> ");
}

int cnt_guavas = 0;
char *guava_gius[MAX_ENTRIES];

void guava() {
    if (cnt_guavas >= MAX_ENTRIES) {
        printf("guava overload\n");
        exit(0);
    }

    printf("how many guavas: ");
    int sz;
    scanf("%d", &sz);
    if (sz >= 0x700) {
        printf("guava overload\n");
        exit(0);
    }

    char *ptr = malloc(sz);

    printf("guavset: ");
    int offset;
    scanf("%d", &offset);

    if (offset < 0 || offset >= sz - 2) {
        printf("guava overload\n");
        exit(0);
    }
    
    printf("guavas: ");
    read(0, ptr + offset, sz - offset);

    guava_gius[cnt_guavas++] = ptr;
}

void gius() {
    printf("guava no: ");
    int idx;
    scanf("%d", &idx);

    if (idx < 0 || idx >= MAX_ENTRIES) {
        printf("guava overload\n");
        exit(0);
    }

    free(guava_gius[idx]);
}

int main() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    for (int i = 0; i < MAX_ENTRIES; i++) {
        guava_gius[i] = NULL;
    }

    int choice;
    banner();
    while (1) {
        menu();
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                guava();
                break;
            case 2:
                gius();
                break;
            case 3:
                exit(0);
            default:
                printf("invalid choice\n");
                break;
        }
    }
}