#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

char license[32];

char correctFirstBytes[9] = "Xsl3BDxP";
char correctSecondBytes[9] = "mzXaPLzR";

char first8Bytes[9];
char second8Bytes[9];

int firstStage(char* input){

	unsigned char processed[8];
    for (int i = 0; i < 8; i++) {
        switch (i % 3) {
            case 0:
                processed[i] = input[i] ^ 0x5A;
                break;
            case 1:
                processed[i] = input[i] + 0x10;
                break;
            case 2:
                processed[i] = input[i] - 0x25;
                break;
        }
        processed[i] = (processed[i] ^ 0x33);
    }

    for (int i = 0; i < 8; i++) {
        if (processed[i] != correctFirstBytes[i]) {
            return 1;
        }
	}

    return 0;
}

int secondStage(char *str) {
    for (int i = 0; i < 8; i++) {
        if (islower(str[i])) {
            str[i] = ((str[i] - 'a' + 5) % 26) + 'a';
        } else if (isupper(str[i])) {
            str[i] = ((str[i] - 'A' - 9 + 26) % 26) + 'A';
        }
    }

	for (int i = 0; i < 8; i++) {
        if (str[i] != correctSecondBytes[i]) {
            return 1;
        }
	}

    return 0;
}

int main(){

	printf("Please enter your license key to use this program!\n");

	fgets(license, 18, stdin);
	size_t len = strlen(license);

	if (len != 17)
		exit(0);

	if (len > 0 && license[len-1] == '\n') {
            license[len-1] = '\0';
    }

	strncpy(first8Bytes, license, 8);
	first8Bytes[8] = '\0'; 

	if (firstStage(first8Bytes) == 1){
		printf("Nope\n");
		exit(0);
	}

	if (license[8] != '-')
		exit(0);

	strncpy(second8Bytes, license+9, 8);
	if (secondStage(second8Bytes) == 1){
		printf("Nope\n");
		exit(0);
	}

	FILE *file;
    char ch;

    file = fopen("./flag.txt", "r");
    if (file == NULL) {
        perror("Error opening file. Open a ticket.\n");
        return EXIT_FAILURE;
    }

    while ((ch = fgetc(file)) != EOF) {
        putchar(ch);
    }

    fclose(file);

	return 0;
}