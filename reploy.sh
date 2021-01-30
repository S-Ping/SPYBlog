#!/usr/bin/env bash

echo "删除旧镜像"
docker stop blog
docker rm blog
docker rmi spy_blog:v1
echo "构建镜像"
docker build -t spy_blog:v1 -f Dockerfile .
echo "启动容器"
mkdir -p /var/log/spy_blog
docker run --name blog -itd -p 6000:6000 -v /var/log:/var/log -v /etc/localtime:/etc/localtime spy_blog:v1
echo "完毕"