# Here's A Libc
> stack buffer overflow  
> ROP (Return-oriented Programing)

ある程度学んでいるとやるだけに見える(らしい)問題

__*以下の解説は、読者の知識量が問題を解く前の私と同程度であることを想定しています。*__


## 解法

* do_stuffにBOF(Buffer overflow)が見える
* `checkseck vuln`をすると、canaryが無いことが分かるので、do_stuffのリターンアドレスを書き換えられそう
* このことを用いて、system('/bin/sh')を呼び出したい
* system()や'/bin/sh'はlibc内に存在しているので、libcの関数がメモリのどこに配置されているのかを知りたい(libc leak)
* これもリターンアドレス書き換えで実現できる
* 以上の二つを送りたいが、一度リターンアドレスを書き換えると二度目は送れないのでは？->これもリターンアドレス書き換えで解決できる
* あとはやるだけ

## Libc leak(一度目のペイロード)
```python
offset = 136
exe = pwn.ELF("./vuln")
pop_rdi = 0x0000000000400913
payload = b'A' * offset
payload += pwn.p64(pop_rdi)
payload += pwn.p64(exe.got["puts"])
payload += pwn.p64(exe.plt["puts"])
payload += pwn.p64(exe.sym["do_stuff"])
```

ROPをやったことがないと「なにこれ？」になります(私がそう)。簡単な(win関数のアドレスに書き換えるだけ)ROPの問題も解いたことがないという場合は、そちらを先に解いてみることをお勧めします。[picoCTF buffer overflow 1](https://play.picoctf.org/practice/challenge/258?category=6&page=2)

### offset
リターンアドレスまでのゴミの長さを指定しています。

### pop_rdi
これは、実行ファイル内に存在する、`pop rdi; ret`という命令のアドレスになります。(実はこのような命令は実行ファイル内にたくさん散らばっていて、`ROPGadget`と呼ばれています。rp++などのツールを使うことで探し出すことができます。)

pop_rdiに入っているのはアドレスですので、`do_stuff`から`pop rdi; ret`という短い関数にリターンするというイメージです。

よって、do_stuffの末尾のretが実行されると、次に実行されるのはこの`pop rdi`です。`pop rdi`によって何が起こるか分かりますか？スタックのポインタは現在`pop rdi`の存在するアドレスを指しているので、その次の`got["puts"]`がrdiレジスタに入ります。`got["puts"]`については、次で解説します。
### got["puts"]
ずばり、`got["puts"]`の意味するところは、libcに存在するputs関数の実体を指すアドレスです。

「GOTってなんや！」私は思いました。この問題に対する様々なwriteupを調べましたが、詳しくは全然書いてありません。これはGOTに触れるなどすると問題の解説の範疇を越えてしまうためだと思っています。よって、私も他の文献に任せます。
* 迷路本
* <https://github.com/wani-hackase/wanictf2020-writeup/tree/master/pwn/04-got-rewriter>

### plt["puts"]
GOTの意味を知っていた、あるいは今知ったあなたは、PLTの意味も理解したことと思います。`plt["puts"]`は、実際に`puts()`を呼び出す際のアドレスになります。先ほどの`pop rdi`により、rdiレジスタには`got["puts"]`が入っていますから、`puts(got["puts"])`がここで実行されます。よってlibc内のputsのアドレスが判明したので、libc内の任意の関数のアドレスも判明しました！

「なんでputs(got["puts"])が実行されるの？」ROPをよく知らない私は思いました。ここで、プログラムの動きを復習します。

`do_stuff`から`main`へのリターンアドレスを`pop rdi; ret`に書き換えましたね。このことにより、rdiにgot["puts"]がセットされ、スタックの先頭もgot["puts"]の部分を指しています。

この次には、`pop rdi; ret`の`ret`の部分が実行されます。これはどこに帰るのでしょうか？それは、stack上の次に書かれているアドレスです。よって、`plt["puts"]`に返る、つまり、puts()が実行されます。

上記と同様の理由で、puts()のリターンアドレスはdo_stuffになっていますから、`puts(glt["puts"])`の次には再度do_stuffが呼ばれます。

## シェル起動(二度目のペイロード)
執筆中！ちょっと待ってね
### ret
なんでretがあるの？->浮動小数点命令(?)みたいのがあるらしく、system()かなんかはこれにあたる。命令のアドレスのアラインメントの関係で、retがないと怒られる。retを挟むといい感じになる。とりあえずretを付けとけばOK！

## 感想
学ぶこと多すぎ！でも楽しい。pwn最高！