import pymysql
import csv
import os
import sys

from google.cloud import storage


def load_a(user,password,hostname,dataset,query,table,destinationBucket):

    #cleaning directory
    dir = '/tmp'
    filelist = [ f for f in os.listdir(dir) if f.endswith(".csv") ]
    for f in filelist:
        os.remove(os.path.join(dir, f))

    db_opts = {
        'user': user,
        'password': password,
        'host': hostname,
        'database': dataset
        }

    db = pymysql.connect(**db_opts)
    cur = db.cursor()

    sql = query
    csv_file_path = '/tmp/'+table+'.csv'
    
    try:
        cur.execute(sql)
        rows = cur.fetchall()
    finally:
        db.close()

    # Continue only if there are rows returned.
    if rows:
        # New empty list called 'result'. This will be written to a file.
        result = list()

        # The row name is the first entry for each entity in the description tuple.
        column_names = list()
        for i in cur.description:
            column_names.append(i[0])

        result.append(column_names)
        for row in rows:
            result.append(row)

        # Write result to file.
        with open(csv_file_path, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in result:
                csvwriter.writerow(row)

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(destinationBucket)
        blob = bucket.blob(table)
        blob.upload_from_filename(csv_file_path)
    else:
        sys.exit("No rows found for query: {}".format(sql))