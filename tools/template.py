import pwn
pwn.context.arch = "amd64"
pwn.context.bits = 64
# pwn.context.log_level = "DEBUG"
# io = pwn.process("./vuln")
# io: pwn.tubes.tube.tube = pwn.gdb.debug(
#     "./vuln", """
#     b *main
#     """,env={"LD_PRELOAD":"./libc.so.6"}
# )
io = pwn.remote("", )
e = pwn.ELF("./vuln")
# libc = pwn.ELF("./libc.so.6")

io.interactive()