import pwn
filepath = "./vuln"
pwn.context.arch = "amd64"
pwn.context.bits = 64
pwn.context.terminal = "tmux splitw -h".split()
# pwn.context.log_level = "DEBUG"
# io = pwn.process(filepath)
# io: pwn.tubes.tube.tube = pwn.gdb.debug(
#     [filepath], """
#     b *main
#     """,env={"LD_PRELOAD":"./libc.so.6"}
# )
io = pwn.remote("", )
# pwn.util.proc.wait_for_debugger(pwn.util.proc.pidof(io)[0])
e = pwn.ELF(filepath)
# libc = pwn.ELF("./libc.so.6")

io.interactive()