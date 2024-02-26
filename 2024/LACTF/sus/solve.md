# sus
> stack buffer overflow \
> ROP (Return-oriented Programing)

__*以下の解説は、読者の知識量が問題を解く前の私と同程度であることを想定しています。*__
私はpicoCTFのHere's A LIBCなどを解いていたので、このwriteupで分からなかった部分はHere's A LIBCのwriteupを読むと良いかもしれません。


## 解法

* 明らかなBOF(Buffer overflow)が見える
* `checkseck sus`をすると、canaryが無いことが分かるので、普通にBOFできる
* このことを用いて、system('/bin/sh')を呼び出したい
* libcリークをしたいので、Dockerfileを持ってきてビルドしてlibc.so.6を持ってくる <- __*最難関*__
* リークしたいのはそうだが、sus 実行ファイルの中に`pop rdi`ガジェットが存在しない(らしい)ので、どうする？
* sus()呼び出しの際にローカル変数をrdiに入れているので、BOFでローカル変数を書き換え
* やるだけ

## libcを持ってくる
Dockerfileがあるので、ビルドしてこの中からlibcを持ってくるという裏技があるらしい。天才じゃん。 \
ここで初心者の私は、`lib/libc.so.6`を持ってきたため、一生を費やしても解けませんでした。`/srv/usr/lib/x86_64-linux-gnu/libc.so.6`から取ってくると良いです。なんで？そういうものです。

## Libc leak(一度目のペイロード)
```python
offset = 0x38
payload += b'A' * offset
payload += pwn.p64(e.got['puts']) # rdi
payload += pwn.p64(1)
payload += pwn.p64(e.plt['puts'])
payload += pwn.p64(e.sym['main'])
io.sendline(payload)
```

ここはやるだけに見えてきて嬉しい。　\
ROPの最初は`e.plt["puts"]`の呼び出しから始まる。実行ファイルのバイナリを読むと分かるが、`e.got["puts"]`を記述した部分にはもともとローカル変数である`u`の値がある部分である。uはsus呼び出しの引数となっているので、sus呼び出しの際に勝手にrdiに入れてくれる。よって、ここに`e.got["puts"]`を入れて`e.plt["puts"]`を呼べばlibcリーク完了である。

## シェル起動(二度目のペイロード)
```python
offset = 0x38
payload += b'A' * offset
payload += pwn.p64(e.got['puts']) # rdi
payload += pwn.p64(1)
payload += pwn.p64(e.plt['puts'])
payload += pwn.p64(e.sym['main'])
io.sendline(payload)
```
これもやるだけ(writeup 書くの 飽きた)

## 解けた！
解けました。