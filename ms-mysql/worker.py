 
import logging
import os
import json

from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from bson import json_util
from services import dbconn
from services import cryptool
from services import sqltostorage

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    logger.info("Init Ok")
    return jsonify("Ingestion Tool API v1")

@app.route("/mysqlingestion", methods=["POST"])
def start_ingest():
    processName = request.json['processName']
    try:
        collection = dbconn.get_on_collection(processName)
        res = json_util.dumps(collection)
        json_object = json.loads(res)

        active = (json_object["active"])
        algorithm = (json_object["algorithm"])
        anonymized = (json_object["anonymized"])
        anonymizedColumns = (json_object["anonymizedColumns"])
        dataset = (json_object["dataset"])
        deleteColumns = (json_object["deleteColumns"])
        destinationBucket = (json_object["destinationBucket"])
        destinationDataset = (json_object["destinationDataset"])
        hostname = (json_object["hostname"])
        nameColumnResult = (json_object["nameColumnResult"])
        encrypted_password_decoded = (json_object["password"])
        port = (json_object["port"])
        processName = (json_object["processName"])
        typeProcess = (json_object["typeProcess"])
        query = (json_object["query"])
        replaceFiles = (json_object["replaceFiles"])
        seed = (json_object["seed"])
        table = (json_object["table"])
        truncateTable = (json_object["truncateTable"])
        typeConnection = (json_object["typeConnection"])
        user = (json_object["user"])

        decrypted_password_decoded = cryptool.decrpyt(encrypted_password_decoded)

        if typeProcess == "sql-to-gcs":
            sqltostorage.load_a(user,decrypted_password_decoded,hostname,dataset,query,table,destinationBucket)
            logger.info('Se cargo el archivo a GCS')

        return jsonify('Done')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)  # TODO: Raise HTTP error

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == "__main__":
    logger.info("Starting Flask App")
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("HTTP_PORT", "5000"))