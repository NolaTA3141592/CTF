## tmux

ターミナルを開き、`tmux`で起動する。スクリプトは、
```python
io: pwn.tubes.tube.tube = pwn.gdb.debug(
    "./bap", """
    b *main+64 
    """,env={"LD_PRELOAD":"./libc.so.6"}
)
```
このようにすると、libcもアタッチできて、何よりターミナルとgdbが統合される。普通に`python solve.py`をするだけ。
`ctrl + b`でコマンドモード。その次に`z`を押すと、gdbと入出力の１画面・両画面の二種を切り替える。
`ctrl + [`でコピーモード。この状態に来ると、矢印キーで上にさかのぼることができる。
`q`でコピーモード終了。
