#!/usr/bin/env python3

def convert_to_luma_asm(data):
	data = data.replace(b"XOR", b"XZD")
	data = data.replace(b"AND", b"LQE")
	data = data.replace(b"ADD", b"RALK")
	data = data.replace(b"SUB", b"MQZL")
	data = data.replace(b"DIV", b"LQDM")
	data = data.replace(b"MUL", b"XKA")
	data = data.replace(b"MOV", b"MISZ")
	data = data.replace(b"INC", b"OAN")
	data = data.replace(b"DEC", b"MAZ")
	data = data.replace(b"CMP", b"VMR")
	data = data.replace(b"MQD", b"MQD")
	data = data.replace(b"FLG", b"FLG")
	return data


from pwn import *
elf = ELF("./virtual-rev")
#p = elf.process()
p = remote('challs.tfcctf.com',30152)

Payload = b'''INC l0
INC l0
MUL l0, l0
MUL l0, l0
MOV l1, l0
MOV l2, l0
MOV l3, l0
MOV l4, l0
INC lax
INC lax
ADD l5,lax
MUL l0, l0
ADD l5,l5
INC l5
MUL l0, l5
INC l5
MUL l1,l5
MUL l2,l5
MUL l3,l5
MUL l4,l5
ADD l0,l1
SUB l0,l5
SUB l0,l5
SUB l0,l5
SUB l0,l5
SUB l0,l5
SUB l0,l5
DEC l0
DEC l0
DEC l0
INC l4
ADD l5,l5
ADD l3,l5
ADD l1,l5
INC l3
ADD l2,l5
ADD l2,l5
SUB l2,lax
DEC l2
FLG
'''
Payload = Payload.replace(b"\t\t\t", b"")
Payload = convert_to_luma_asm(Payload)
p.sendline(Payload)


p.interactive()