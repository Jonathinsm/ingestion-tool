#!/bin/bash
echo --------------------------------
echo ------------Limpiando imagenes
echo --------------------------------
docker rmi $(docker images | grep mongo) --force
echo --------------------------------
echo ------------Creado docker
echo --------------------------------
docker-compose -f ms-db-docker-compose.yml build

echo --------------------------------
echo ------------Push a Container Registry
echo --------------------------------
docker tag mongo:4.2 gcr.io/$PROJECT_ID/mongo:4.2
gcloud docker -- push gcr.io/$PROJECT_ID/mongo:4.2

echo --------------------------------
echo ------------Desplegando Microservicio
echo --------------------------------
kubectl delete deployment ms-db -n ingestion-tool
sleep 10
kubectl apply -f k8s/ -n ingestion-tool