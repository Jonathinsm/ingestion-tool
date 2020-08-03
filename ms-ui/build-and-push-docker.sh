#!/bin/bash
echo --------------------------------
echo ------------Limpiando imagenes
echo --------------------------------
docker rmi $(docker images | grep ms-ui) --force
echo --------------------------------
echo ------------Creado docker
echo --------------------------------
docker-compose -f ms-ui-docker-compose.yml build

echo --------------------------------
echo ------------Push a Container Registry
echo --------------------------------
docker tag ms-ui:latest gcr.io/$PROJECT_ID/ms-ui:latest
gcloud docker -- push gcr.io/$PROJECT_ID/ms-ui:latest

echo --------------------------------
echo ------------Desplegando Microservicio
echo --------------------------------
kubectl delete deployment ms-ui -n ingestion-tool
sleep 10
kubectl apply -f k8s/ -n ingestion-tool