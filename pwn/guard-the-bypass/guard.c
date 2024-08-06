#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>	
#include <unistd.h>

__asm__(
"pop %rdi\n\t"
"ret");

void setup(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int get_len(){

	int len;
	fputs("Select the len: ", stdout);
	scanf("%d", &len);
	return len;

}
int len;
void game(void){
	
	char buf[32] = {0};
	getchar();
	read(0, buf, len);

}

// gcc guard.c -o guard -no-pie
void main(void){

	setup();
	int choice;
	puts("Welcome! Press 1 to start the chall.");
	scanf("%d", &choice);
	if (choice != 1){
		puts("Bye!");
		exit(0);
	}
	else{
		len = get_len();
		pthread_t p;
		pthread_create(&p, NULL, (void*)game, NULL);
		pthread_join(p, NULL);

	}
}
