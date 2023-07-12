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

## 補足

本当はレイヤーごとに適切な単体テストを実施したいが、今回は省略した。  
また、テストを意識するとオニオンアーキテクチャで書きたくなる。  
FastAPIでオニオンアーキテクチャを採用しているサンプルコードはあまり見つからなかったが、[こちら](https://techblog.raksul.com/entry/2023/06/30/142904)が参考になりそう。
