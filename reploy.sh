#!/usr/bin/env bash

echo "删除旧镜像"
docker stop blog
docker rm blog
docker rmi spy_blog:blog
echo "构建镜像"
docker build -t spy_blog:blog -f Dockerfile .
echo "启动容器"
mkdir -p /var/log/spy_blog
docker run --name blog -m 6G -itd -p 6000:6000 -v /var/log:/var/log -v /etc/localtime:/etc/localtime spy_blog:blog
echo "完毕"