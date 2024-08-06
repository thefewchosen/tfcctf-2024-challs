#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include "stdio.h"

int main() {
	char buffer[0x78];
	read(0, buffer, 0x78);
	
	char magic[0x8] = { 0x7f, 0x45, 0x4c, 0x46, 0x02, 0x01, 0x01, 0x00 };

	for (int i=0;i<8;i++) {
		if (magic[i] != buffer[i]) {
			write(1, "Not an ELF file\n", 16);
			exit(1);
		}
	}

	int fd = memfd_create("program", 0);
	if (fd == -1) {
		write(1, "Failed to create memfd\n", 23);
		exit(1);
	}
	write(fd, buffer, 0x78);
	
	const char * const argv[] = {NULL};
	const char * const envp[] = {NULL};
	
	int error = fexecve(fd, argv, envp);

	if (error == -1) {
		write(1, "Failed to execute\n", 18);
		exit(1);
	}
}
