#!/usr/bin/env python3

from pwn import *

elf = ELF('./license')
#p = elf.process()
p = remote('challs.tfcctf.com',31882)

correct8Bytes = "Xsl3BDxP"

firstStage = bytearray(8)


for i in range(0, len(correct8Bytes)):
	firstStage[i] = ord(correct8Bytes[i]) ^ 0x33
	if (i % 3 == 0):
		firstStage[i] = firstStage[i] ^ 0x5a
	elif (i % 3 == 1):
		firstStage[i] = firstStage[i] - 0x10
		print(firstStage[i])
	elif (i % 3 == 2):
		firstStage[i] = firstStage[i] + 0x25

firstStage += b'-'

correct8Bytes = 'mzXaPLzR'
for i in range(0, len(correct8Bytes)):
	if correct8Bytes[i].islower():
		firstStage += chr(((ord(correct8Bytes[i]) - ord('a') - 5) % 26) + ord('a')).encode()
	else:
		firstStage += chr(((ord(correct8Bytes[i]) - ord('A') + 9) % 26) + ord('A')).encode()

# gdb.attach(p, gdbscript='''b * secondStage+333
# b * main+194
# b * main+67''')
print(firstStage)
p.sendline(firstStage)

p.interactive()