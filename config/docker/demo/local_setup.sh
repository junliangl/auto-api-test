#!bin/bash

echo ========== 开始构建本地 mysql docker ==========

DOCKER_PORT=3307
DOCKER_IMAGES=`docker images -aq --no-trunc --filter=reference="demo"`
DOCKER_CONTAINERS=`docker ps -aq --no-trunc --filter=name="demo"`
PORT_INFO=`docker ps -aq --no-trunc --filter=publish=$DOCKER_PORT`

if [[ ! $PORT_INFO ]]; then
  echo port $DOCKER_PORT is ok
else
  docker stop $PORT_INFO
fi

if [[ ! $DOCKER_CONTAINERS ]]; then
  echo local "mysql-demo" docker container is null
else
  docker stop $DOCKER_CONTAINERS
  docker rm $DOCKER_CONTAINERS
  docker volume rm $(docker volume ls -q)
fi

if [[ ! $DOCKER_IMAGES ]]; then
  echo local docker images is null
else
  docker rmi $DOCKER_IMAGES
fi

docker build -f config/docker/demo/mysql.Dockerfile -t mysql-demo:test .

docker run -d -p 3307:3306 --name=demo mysql-demo:test

docker logs $(docker ps -lq)

echo ========== 以下是构建的 mysql docker ==========

docker ps -l

echo ========== 完成构建本地 mysql docker ==========

docker logs -f $(docker ps -lq)