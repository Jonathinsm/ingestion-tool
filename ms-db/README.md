# Ms-db for ingestion tool

Work in Progress

## Setup Nescesary for DB:

1. Connect to container.
```
kubectl exec -it  pod_id sh
docker exec -it  cont_id sh
```

2. Connect to DB.
```
mongo --username root --password test
```

3. Use DB.
```
use db_pruebas
```

4. Create Index Database.
```
db.connections.createIndex( { processName: 1 }, { unique: true } )
```