# eval-tar-pax
ファイルを含むデータをストリームで効率よく送受信するためのフォーマットとして、tarを検討。
エントリ毎にメタデータを付与できるPAXの仕様を利用したく、JS, Go, Pythonのそれぞれで適切に取り扱うことができることを検証。

## How to test
### client(JS)のセットアップ
```bash
$ cd client
$ pnpm install
$ pnpm dev
```

### server(Go) + tool(Python)のセットアップ
```bash
$ cd tool; uv sync; cd -
$ cd server; go run main.go
```

### テスト
```bash
$ curl http://localhost:8787/
```

### 出力
#### client(JS)
```bash
target: a
target: b
target: c
target: d
target: e
Returned entries:
Entry: a, Type: file, Size: 1048576
PAX header: {"customHeader":"a"}

Entry: b, Type: file, Size: 1048576
PAX header: {"customHeader":"b"}

Entry: c, Type: file, Size: 1048576
PAX header: {"customHeader":"c"}

Entry: d, Type: file, Size: 1048576
PAX header: {"customHeader":"d"}

Entry: e, Type: file, Size: 1048576
PAX header: {"customHeader":"e"}
```

#### server(Go) + tool(Python)
```bash
=============================================================
Content-Type: application/x-tar
Transfer-Encoding: 

Received entry: a, Type: b'0', Size: 1048576
PAX headers: [('customHeader', 'a')]
Received entry: b, Type: b'0', Size: 1048576
PAX headers: [('customHeader', 'b')]
Received entry: c, Type: b'0', Size: 1048576
PAX headers: [('customHeader', 'c')]
Received entry: d, Type: b'0', Size: 1048576
PAX headers: [('customHeader', 'd')]
Received entry: e, Type: b'0', Size: 1048576
PAX headers: [('customHeader', 'e')]
```
