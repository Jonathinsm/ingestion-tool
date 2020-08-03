 
import logging
import os
import json
import requests

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from bson import json_util
from services import dbconn
from services import cryptool

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/")
def health():
    logger.info("Health Check")
    return jsonify("Ok")

@app.route("/api/v1")
def api():
    logger.info("Init Ok")
    return jsonify("Ingestion Tool API v1")

@app.route("/api/v1/connections", methods=["GET"])
def get_connections():
    try:
        collections = dbconn.get_all_collections()
        res = json_util.dumps(collections)
        logger.info("Documentos Obetnidos")
        return Response(res, mimetype='application/json')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.route("/api/v1/connection", methods=["POST"])
def get_connection_info():
    id = request.json['id']

    try:
        collection = dbconn.get_on_collection(id)
        res = json_util.dumps(collection)
        json_object = json.loads(res)
        encrypted_password_decoded = (json_object["password"])
        decrypted_password_decoded = cryptool.decrpyt(encrypted_password_decoded)
        planepassword = { "passwordplane" : decrypted_password_decoded }
        resu = json.loads(res)
        resu.update(planepassword)
        newres = json.dumps(resu)
        logger.info("Registro obtenido %s", newres)
        return Response(newres, mimetype='application/json')
        return jsonify('ok')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.route("/api/v1/newconnection", methods=["POST"])
def new_connection():
    active = request.json['active']
    algorithm = request.json['algorithm']
    anonymized = request.json['anonymized']
    anonymizedColumns = request.json['anonymizedColumns']
    dataset = request.json['dataset']
    deleteColumns = request.json['deleteColumns']
    destinationBucket = request.json['destinationBucket']
    destinationDataset = request.json['destinationDataset']
    hostname = request.json['hostname']
    nameColumnResult = request.json['nameColumnResult']
    password = request.json['password']
    port = request.json['port']
    processName = request.json['processName']
    typeProcess = request.json['typeProcess']
    query = request.json['query']
    replaceFiles = request.json['replaceFiles']
    seed = request.json['seed']
    table = request.json['table']
    truncateTable = request.json['truncateTable']
    typeConnection = request.json['typeConnection']
    user = request.json['user']

    encrypted_password_decoded = cryptool.encrpyt(password)

    data = {
        'active': active,
        'algorithm': algorithm,
        'anonymized': anonymized,
        'anonymizedColumns': anonymizedColumns,
        'dataset': dataset,
        'deleteColumns': deleteColumns,
        'destinationBucket': destinationBucket,
        'destinationDataset': destinationDataset,
        'hostname': hostname,
        'nameColumnResult': nameColumnResult,
        'password': encrypted_password_decoded,
        'port': port,
        'processName': processName,
        'typeProcess': typeProcess,
        'query': query,
        'replaceFiles': replaceFiles,
        'seed': seed,
        'table': table,
        'truncateTable': truncateTable,
        'typeConnection': typeConnection,
        'user': user
    }

    try:
        res = json_util.dumps(dbconn.new_documment(data))
        logger.info('Conexion guardada %s', res)
        return Response(res,mimetype='application/json')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.route("/api/v1/updateconnection", methods=["POST"])
def update_connection():

    active = request.json['active']
    algorithm = request.json['algorithm']
    anonymized = request.json['anonymized']
    anonymizedColumns = request.json['anonymizedColumns']
    dataset = request.json['dataset']
    deleteColumns = request.json['deleteColumns']
    destinationBucket = request.json['destinationBucket']
    destinationDataset = request.json['destinationDataset']
    hostname = request.json['hostname']
    nameColumnResult = request.json['nameColumnResult']
    password = request.json['password']
    port = request.json['port']
    processName = request.json['processName']
    typeProcess = request.json['typeProcess']
    query = request.json['query']
    replaceFiles = request.json['replaceFiles']
    seed = request.json['seed']
    table = request.json['table']
    truncateTable = request.json['truncateTable']
    typeConnection = request.json['typeConnection']
    user = request.json['user']

    encrypted_password_decoded = cryptool.encrpyt(password)

    filter =  {"processName": processName }
    newvalues = {
        "$set": {
            'active': active,
            'algorithm': algorithm,
            'anonymized': anonymized,
            'anonymizedColumns': anonymizedColumns,
            'dataset': dataset,
            'deleteColumns': deleteColumns,
            'destinationBucket': destinationBucket,
            'destinationDataset': destinationDataset,
            'hostname': hostname,
            'nameColumnResult': nameColumnResult,
            'password': encrypted_password_decoded,
            'port': port,
            'processName': processName,
            'typeProcess': typeProcess,
            'query': query,
            'replaceFiles': replaceFiles,
            'seed': seed,
            'table': table,
            'truncateTable': truncateTable,
            'typeConnection': typeConnection,
            'user': user
        } 
    }
    try:
        res = dbconn.update_documment(filter,newvalues)
        logger.info("Actualizacion correcta %s", res)
        return jsonify('Actualizado')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.route("/api/v1/deleteconnection", methods=["POST"])
def delete_connection():
    id = request.json['id']

    try:
        res = dbconn.delete_documment(id)
        logger.info("Registro Eliminado %s", res)
        return jsonify('Deleted')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.route("/api/v1/ingestdata", methods=["POST"])
def sqltostorage():
    processName = request.json["processName"]
    hostname = os.environ['MSMYSQL_HOSTNAME']
    url = "http://"+hostname+":5000/mysqlingestion"

    try:
        collection = dbconn.get_on_processname(processName)
        res = json_util.dumps(collection)
        json_object = json.loads(res)
        typeConnection = (json_object["typeConnection"])
        payload = {'processName':processName}
        
        if typeConnection == "mysql":
            x = requests.post(url, json=payload)
            logger.info(x.text)

        return jsonify('ok')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == "__main__":
    logger.info("Starting Flask App")
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("HTTP_PORT", "5000"))