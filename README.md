# Ingestion tool

This is a tool for ingest data in to Google Cloud Platform. The application is based in Flask Micro Framework.!The work is in progress yet!.
The tool will be able to extract data from different data sources that exist in the market in batch and save it in Gcp.

## Application Architecture

![alt text](https://github.com/jonathinsm/ingestion-tool/blob/master/img/ingestion-tool-App-Arch.png?raw=true)

## GCP Arcchitecture

![alt text](https://github.com/jonathinsm/ingestion-tool/blob/master/img/ingestion-tool-Gcp-Arch.png?raw=true)

## Prerequisites:
* Python 3.6 or higger
* Docker
* Google SDK

## How to run locally:
1. Set the environment variables refer to the env-variables file for guidance.
2. Desploy ms-db to docker and setup the database use the README file in the ms-db.
3. Deploy each python microservice independly Read the README of each microservice.


## How to run in GCP:
1. Install the Google SDK in your computer or use the Cloud Shell.
2. Log In in your GCP project wiht the righ permissions (Editor, Owner).
1. Set the environment variables refer to the env-variables file for guidance.
2. Run the deploy-project file.
```
sh deploy-project.sh
```
3. Setup the database use the README file in the ms-db.
