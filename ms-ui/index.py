import logging
import os
import requests
import json

from  flask import Flask, jsonify, request, render_template, redirect, url_for

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

#Reenderizar todas las conexiones
@app.route('/connections')
def connections():
    hostname = os.environ['MSCONTROLLER_HOSTNAME']
    url = "http://"+hostname+":5000/api/v1/connections"

    try:
        r = requests.get(url)
        data = json.loads(r.text)
        return render_template('connections.html', data=data)
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)

#Retornar el formulario de nueva conexión
@app.route('/newconnection')
def newconnection():
    return render_template('forms.html')

#Enviar los datos de la nueva conexión
@app.route('/saveconn', methods=['POST'])
def saveconn():
    hostname = os.environ['MSCONTROLLER_HOSTNAME']
    url = "http://"+hostname+":5000/api/v1/newconnection"

    active = request.form['active']
    algorithm = request.form['algorithm']
    anonymized = request.form['anonymized']
    anonymizedColumns = request.form['anonymizedColumns']
    dataset = request.form['dataset']
    deleteColumns = request.form['deleteColumns']
    destinationBucket = request.form['destinationBucket']
    destinationDataset = request.form['destinationDataset']
    hostname = request.form['hostname']
    nameColumnResult = request.form['nameColumnResult']
    password = request.form['password']
    port = request.form['port']
    processName = request.form['processName']
    typeProcess = request.form['typeProcess']
    query = request.form['query']
    replaceFiles = request.form['replaceFiles']
    seed = request.form['seed']
    table = request.form['table']
    truncateTable = request.form['truncateTable']
    typeConnection = request.form['typeConnection']
    user = request.form['user']

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
        'password': password,
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
        r = requests.post(url, json=data)
        logger.info(r.text)
        return redirect(url_for('connections'))
        #return render_template('connections.html')

    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)

#Retornar el formulario de actualizar conexión
@app.route('/updateconnection')
def updateconnection():
    id = request.args.get("id")
    hostname = os.environ['MSCONTROLLER_HOSTNAME']
    url = "http://"+hostname+":5000/api/v1/connection"
    
    payload = {"id":id}
    logger.info(payload)
    try:
        r = requests.post(url, json=payload)
        logger.info(r.text)
        
        data = json.loads(r.text)
        return render_template('forms.html', data=data)
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)

#Enviar los datos de actualización de conexión
@app.route('/updateconn', methods=['POST'])
def updateconn():
    hostname = os.environ['MSCONTROLLER_HOSTNAME']
    url = "http://"+hostname+":5000/api/v1/updateconnection"
    url_tool = os.environ['MSCONTROLLER_HOSTNAME']

    active = request.form['active']
    algorithm = request.form['algorithm']
    anonymized = request.form['anonymized']
    anonymizedColumns = request.form['anonymizedColumns']
    dataset = request.form['dataset']
    deleteColumns = request.form['deleteColumns']
    destinationBucket = request.form['destinationBucket']
    destinationDataset = request.form['destinationDataset']
    hostname = request.form['hostname']
    nameColumnResult = request.form['nameColumnResult']
    password = request.form['password']
    port = request.form['port']
    processName = request.form['processName']
    typeProcess = request.form['typeProcess']
    query = request.form['query']
    replaceFiles = request.form['replaceFiles']
    seed = request.form['seed']
    table = request.form['table']
    truncateTable = request.form['truncateTable']
    typeConnection = request.form['typeConnection']
    user = request.form['user']

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
        'password': password,
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
        r = requests.post(url, json=data)
        logger.info(r.text)
        return redirect(url_for('connections'))
        #return render_template('connections.html')

    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)

#Enviar conexión a eliminar
@app.route('/deleteconection')
def deleteconection():
    id = request.args.get("id")
    hostname = os.environ['MSCONTROLLER_HOSTNAME']
    url = "http://"+hostname+":5000/api/v1/deleteconnection"
    
    payload = {"id":id}
    logger.info(payload)
    try:
        r = requests.post(url, json=payload)
        logger.info(r.text)
        data = json.loads(r.text)
        return redirect(url_for('connections'))
        #return render_template('connections.html')
        
    except Exception as ex:
        logger.error("Exception: %s", ex)
        return jsonify("Error %s" % ex)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get("HTTP_PORT", "5000"))