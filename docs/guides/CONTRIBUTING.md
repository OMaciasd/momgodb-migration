# **Migration Guide: PostgreSQL to MongoDB** 🚀

This guide provides a detailed process for migrating data from PostgreSQL to MongoDB using Python. The migration consists of three main steps:

1. Exporting data from PostgreSQL.
2. Transforming the data into the required MongoDB format.
3. Importing the data into MongoDB.

## **Contents** 📚

- [**Migration Guide: PostgreSQL to MongoDB** 🚀](#migration-guide-postgresql-to-mongodb-)
  - [**Contents** 📚](#contents-)
  - [🧩 **Project Structure**](#-project-structure)
  - [🔑 **Prerequisites**](#-prerequisites)
  - [Steps for Migrating Data from PostgreSQL to MongoDB](#steps-for-migrating-data-from-postgresql-to-mongodb)
    - [1. Exporting Data from PostgreSQL](#1-exporting-data-from-postgresql)
      - [Example Python Script (`export_pg_data.py`)](#example-python-script-export_pg_datapy)
  - [🔄 **Transforming Data to JSON Format**](#-transforming-data-to-json-format)
  - [⚙️ **Pasos para Migrar Datos de PostgreSQL a MongoDB**](#️-pasos-para-migrar-datos-de-postgresql-a-mongodb)
    - [📥 **Conexión a MongoDB**](#-conexión-a-mongodb)
  - [1. Export Data from PostgreSQL (`export_pg_data.py`)](#1-export-data-from-postgresql-export_pg_datapy)
    - [**2. Transform Data (`transform_data.py`)**](#2-transform-data-transform_datapy)
    - [**3. Import Data into MongoDB (`import_mongo.py`)**](#3-import-data-into-mongodb-import_mongopy)

## 🧩 **Project Structure**

The project folder will have the following structure:

```plaintext
/migration
  ├── export_pg_data.py
  ├── transform_data.py
  ├── import_mongo.py
  └── config/
      ├── postgres_config.json
       connection
      └── mongo_config.json
      connection

```

## 🔑 **Prerequisites**

Before starting the migration, make sure you have the following installed:

- **PostgreSQL** (source database)
- **MongoDB** (destination database)
- **Python** (with `psycopg2`, `pymongo`, and `pandas` libraries)

Install the necessary Python libraries:

```bash
pip install psycopg2 pandas pymongo

```

## Steps for Migrating Data from PostgreSQL to MongoDB

### 1. Exporting Data from PostgreSQL

To export data from PostgreSQL, you need to connect to the database and extract the required data.

#### Example Python Script (`export_pg_data.py`)

```python
import psycopg2
import json
import pandas as pd

with open('config/postgres_config.json') as f:
    postgres_config = json.load(f)

conn = psycopg2.connect(
    host=postgres_config['host'],
    database=postgres_config['database'],
    user=postgres_config['user'],
    password=postgres_config['password']
)

def export_data(query):
    df = pd.read_sql(query, conn)
    return df.to_dict(orient='records')

data = export_data('SELECT * FROM your_table')

with open('exported_data.json', 'w') as f:
    json.dump(data, f)

conn.close()

```

## 🔄 **Transforming Data to JSON Format**

PostgreSQL data is usually stored in relational tables, while MongoDB uses a flexible JSON-like document model. You will need to transform the data into the MongoDB document format.

```python
import json

with open('exported_data.json', 'r') as f:
    data = json.load(f)

# 1. Flatten nested data
# 2. Rename fields to fit MongoDB schema

with open('transformed_data.json', 'w') as f:
    json.dump(data, f)

```

## ⚙️ **Pasos para Migrar Datos de PostgreSQL a MongoDB**

### 📥 **Conexión a MongoDB**

Usa la librería `pymongo` de Python para conectarte a MongoDB e insertar datos:

```python
from pymongo import MongoClient
import json

with open('config/mongo_config.json') as f:
    mongo_config = json.load(f)

client = MongoClient(mongo_config['uri'])
db = client[mongo_config['database']]
collection = db[mongo_config['collection']]

with open('transformed_data.json', 'r') as f:
    data = json.load(f)

collection.insert_many(data)

client.close()

```

## 1. Export Data from PostgreSQL (`export_pg_data.py`)

```python
import psycopg2
import pandas as pd
import json

def export_postgres_data():
    with open('config/postgres_config.json') as f:
        config = json.load(f)

    conn = psycopg2.connect(
        host=config['host'],
        database=config['database'],
        user=config['user'],
        password=config['password']
    )

    query = 'SELECT * FROM your_table'
    df = pd.read_sql(query, conn)
    conn.close()

    data = df.to_dict(orient='records')
    with open('exported_data.json', 'w') as f:
        json.dump(data, f)

if __name__ == "__main__":
    export_postgres_data()

```

### **2. Transform Data (`transform_data.py`)**

```python
import json

def transform_data():
    with open('exported_data.json', 'r') as f:
        data = json.load(f)

    transformed_data = [
        { "new_field_name": item["old_field_name"] } for item in data
    ]

    with open('transformed_data.json', 'w') as f:
        json.dump(transformed_data, f)

if __name__ == "__main__":
    transform_data()

```

### **3. Import Data into MongoDB (`import_mongo.py`)**

```python
from pymongo import MongoClient
import json

def import_to_mongo():
    with open('config/mongo_config.json') as f:
        config = json.load(f)

    client = MongoClient(config['uri'])
    db = client[config['database']]
    collection = db[config['collection']]

    with open('transformed_data.json', 'r') as f:
        data = json.load(f)

    collection.insert_many(data)
    client.close()

if __name__ == "__main__":
    import_to_mongo()

```
