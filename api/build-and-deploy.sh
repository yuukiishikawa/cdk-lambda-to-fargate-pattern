#!/bin/bash

# 最初の引数をAWSアカウントIDとして使用
AWS_ACCOUNT_ID=$1

if [ -z "$AWS_ACCOUNT_ID" ]; then
    echo "AWSアカウントIDが指定されていません。"
    exit 1
fi

aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com

docker build -t fargate-api-repo --platform linux/x86_64 . --no-cache
docker tag fargate-api-repo:latest $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/fargate-api-repo:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/fargate-api-repo:latest