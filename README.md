# fast-api-expt

## 概要
[terraform-expt](https://github.com/uekiGityuto/terraform-expt)で稼働させる[FastAPI](https://fastapi.tiangolo.com/ja/)のアプリケーション

## デプロイ
terraform-exptで作成したECRにimageをpushする

```sh
docker build -t fast-api-expt .

export AWS_DEFAULT_REGION="ap-northeast-1"
export AWS_ACCESS_KEY_ID="xxx"
export AWS_SECRET_ACCESS_KEY="xxx"
export AWS_SESSION_TOKEN="xxx"

aws --region ap-northeast-1 ecr get-login-password | docker login --username AWS --password-stdin 428485887053.dkr.ecr.ap-northeast-1.amazonaws.com
docker tag fast-api-expt:latest 428485887053.dkr.ecr.ap-northeast-1.amazonaws.com/stg-terraform-expt:latest
docker push 428485887053.dkr.ecr.ap-northeast-1.amazonaws.com/stg-terraform-expt:latest
```

なお、最後に確認した時点から大幅に変更しているので、現状のDockerfileでは適切に起動しない可能性が高い。
また、Code Pipelineの中でDBマイグレーションをするようにすべきだが、それも書いていない。

## 補足

### アーキテクチャ
ui層、usecase層、repository層が一方通行になるようなレイヤードアーキテクチャもどきで書いている。  
テストが書きづらかったら、オニオンアーキテクチャに直したい。  
FastAPIでオニオンアーキテクチャを採用しているサンプルコードはあまり見つからなかったが、[こちら](https://techblog.raksul.com/entry/2023/06/30/142904)が参考になりそう。

### テスト
本当はレイヤーごとに適切な単体テストを実施したいが、今回は省略した。  

### シグナルハンドリング
Graceful Shutdownのためにシグナルハンドリングが必要だが、Uvicornのデフォルトでシグナルハンドリングしているらしい。  
公式ドキュメントには書いてなさそうだったが、[Githubのソース](https://github.com/encode/uvicorn/blob/master/uvicorn/server.py)を読むと確かにそれらしき処理が書いてある。

また、Shutdown処理の前に特別な処理が必要な場合は、Shutdownイベントのハンドリングができるので、それを利用する。（[参考](https://fastapi.tiangolo.com/advanced/events/)）

### ロギング
アクセスログとエラーログを出力している。  
ただ、なぜかDIの中でロギングができない。（そういうもの？）  
`app.ui.errors.handle_error`でエラー処理を共通化しているが、DIで注入した処理から`handle_error`を呼び出してもロギングされない。

### トランザクション
all-or-nothingの思想に基づき、エラーが起きた場合にロールバックするようにした。  
ただ、FastAPIのトランザクション管理について、ベストプラクティスが見つからなかったので、本番運用したときに問題がないかは少し不安。

### バリデーション
簡単なバリデーション（Emailなど）のみ実装した。

### エラーハンドリング
簡単なエラーハンドリングのみ実装した。
