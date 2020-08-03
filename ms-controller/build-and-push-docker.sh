#!/bin/bash
echo --------------------------------
echo ------------Limpiando imagenes
echo --------------------------------
docker rmi $(docker images | grep ms-controller) --force
echo --------------------------------
echo ------------Creado docker
echo --------------------------------
docker-compose -f ms-controller-docker-compose.yml build

echo --------------------------------
echo ------------Push a Container Registry
echo --------------------------------
docker tag ms-controller:latest gcr.io/$PROJECT_ID/ms-controller:latest
gcloud docker -- push gcr.io/$PROJECT_ID/ms-controller:latest

echo --------------------------------
echo ------------Desplegando Microservicio
echo --------------------------------
kubectl delete deployment ms-controller -n ingestion-tool
sleep 10
kubectl apply -f k8s/ -n ingestion-tool