#!/bin/bash

echo --------------------------------
echo ------------Creando Cuenta de Servicio
echo --------------------------------
export SA_NAME="sa-"$CLUSTER_NAME

gcloud iam service-accounts create $SA_NAME \
    --description="Cuenta de Servicio para cluster de Ingesta" \
    --display-name=$SA_NAME

export SA_K8S=$SA_NAME"@"$PROJECT_ID".iam.gserviceaccount.com"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SA_K8S --role=roles/editor

echo --------------------------------
echo ------------Creando Cluter
echo --------------------------------
gcloud beta container clusters create $CLUSTER_NAME \
--zone $ZONE \
--no-enable-basic-auth \
--cluster-version "1.15.12-gke.2" \
--machine-type "e2-medium" \
--image-type "COS" \
--disk-type "pd-standard" \
--disk-size "100" \
--metadata disable-legacy-endpoints=true \
--service-account $SA_K8S \
--num-nodes "2" \
--enable-stackdriver-kubernetes \
--enable-ip-alias \
--network $NETWORK \
--subnetwork $SUBNETWORK \
--enable-autoupgrade \
--enable-autorepair
sleep 10

echo --------------------------------
echo ------------Obteniendo Credenciales
echo --------------------------------
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE

echo --------------------------------
echo ------------Creando Disco Persistente para DB
echo --------------------------------
gcloud beta compute disks create mongo-disk \
--type=pd-ssd \
--size=10GB \
--zone=$ZONE

echo --------------------------------
echo ------------Creando Namespace
echo --------------------------------
kubectl create namespace ingestion-tool

echo --------------------------------
echo ------------Desplegando Secret
echo --------------------------------
kubectl apply -f config/secret.yaml -n ingestion-tool

echo --------------------------------
echo ------------Desplegando ms-db
echo --------------------------------
cd ms-db
sh build-and-push-docker.sh
cd ..

echo --------------------------------
echo ------------Desplegando ms-mysql
echo --------------------------------
cd ms-mysql
sh build-and-push-docker.sh
cd ..

echo --------------------------------
echo ------------Desplegando ms-controller
echo --------------------------------
cd ms-controller
sh build-and-push-docker.sh
cd ..

echo --------------------------------
echo ------------Desplegando ms-ui
echo --------------------------------
cd ms-ui
sh build-and-push-docker.sh
cd ..

echo --------------------------------
echo ------------Desplegando Endpoint
echo --------------------------------
cd config

gcloud compute addresses create ingestion-public-ip \
--project=$PROJECT_ID \
--global

export INGRESS_IP=$(gcloud compute addresses list | grep ingestion-public-ip | grep -o '[0-9]\+[.][0-9]\+[.][0-9]\+[.][0-9]\+')

export ENDPOINT_URL="ingestion-a.endpoints."$PROJECT_ID".cloud.goog"

sed "s, ENDPOINT_URL, '$ENDPOINT_URL',g" openapi.yaml > tempopenapi.yaml
sed "s, INGRESS_IP, '$INGRESS_IP',g" tempopenapi.yaml > resultopenapi.yaml

gcloud endpoints services deploy resultopenapi.yaml

sed "s, INGESS_HOST, '$ENDPOINT_URL',g" ingress.yaml > resultingress.yaml

echo --------------------------------
echo ------------Desplegando Ingress
echo --------------------------------
kubectl apply -f resultingress.yaml -n ingestion-tool

rm tempopenapi.yaml
rm resultopenapi.yaml
rm resultingress.yaml

echo --------------------------------
echo ------------Despliegue Terminado
echo --------------------------------