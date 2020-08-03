#!/bin/bash
echo --------------------------------
echo ------------Limpiando imagenes
echo --------------------------------
docker rmi $(docker images | grep ms-mysql) --force
echo --------------------------------
echo ------------Creado docker
echo --------------------------------
docker-compose -f ms-mysql-docker-compose.yml build

echo --------------------------------
echo ------------Push a Container Registry
echo --------------------------------
docker tag ms-mysql:latest gcr.io/$PROJECT_ID/ms-mysql:latest
gcloud docker -- push gcr.io/$PROJECT_ID/ms-mysql:latest

echo --------------------------------
echo ------------Desplegando Microservicio
echo --------------------------------
kubectl delete deployment ms-mysql -n ingestion-tool
sleep 10
kubectl apply -f k8s/ -n ingestion-tool