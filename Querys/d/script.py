import psycopg2
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt

postgres_config = {
    "dbname": "mi_base_de_datos",
    "user": "mi_usuario",
    "password": "mi_contraseña",
    "host": "localhost",
    "port": 5432
}

mongo_config = {
    "host": "localhost",
    "port": 27017,
    "db_name": "mi_base_mongo"
}


def connect_postgres(config):
    return psycopg2.connect(
        dbname=config["dbname"],
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"]
    )


def connect_mongo(config):
    client = MongoClient(config["host"], config["port"])
    return client[config["db_name"]]


def query_postgres(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def query_mongo(db, pipeline):
    return list(db.orders.aggregate(pipeline))


def save_results_to_txt(results, file_name):
    with open(file_name, "w") as file:
        for result in results:
            file.write(str(result) + "\n")


def generate_graph(data, title, file_name):
    df = pd.DataFrame(data, columns=["Category", "Count"])
    df.plot(kind="bar", x="Category", y="Count", legend=False, title=title)
    plt.savefig(file_name)
    plt.close()


try:
    postgres_conn = connect_postgres(postgres_config)
    mongo_db = connect_mongo(mongo_config)

    category_query_pg = """
        SELECT c.name AS category_name, COUNT(p.product_id) AS product_count
        FROM products p
        INNER JOIN product_categories c ON p.category_id = c.category_id
        GROUP BY c.name;
    """
    warehouse_query_pg = """
        SELECT w.name AS warehouse_name, COUNT(oi.product_id) AS product_count
        FROM orders o
        INNER JOIN order_items oi ON o.order_id = oi.order_id
        INNER JOIN inventories i ON oi.product_id = i.product_id
        INNER JOIN warehouse w ON i.warehouse_id = w.warehouse_id
        WHERE w.name = 'Central Warehouse'
        GROUP BY w.name;
    """

    pg_results_category = query_postgres(postgres_conn, category_query_pg)
    pg_results_warehouse = query_postgres(postgres_conn, warehouse_query_pg)

    category_pipeline_mongo = [
        {"$lookup": {"from": "product_categories", "localField": "category_id", "foreignField": "_id", "as": "category"}},
        {"$unwind": "$category"},
        {"$group": {"_id": "$category.name", "product_count": {"$sum": 1}}}
    ]
    warehouse_pipeline_mongo = [
        {"$unwind": "$items"},
        {"$lookup": {"from": "inventories", "localField": "items.product_id", "foreignField": "product_id", "as": "inventory"}},
        {"$unwind": "$inventory"},
        {"$lookup": {"from": "warehouse", "localField": "inventory.warehouse_id", "foreignField": "_id", "as": "warehouse"}},
        {"$unwind": "$warehouse"},
        {"$match": {"warehouse.name": "Central Warehouse"}},
        {"$group": {"_id": "$warehouse.name", "product_count": {"$sum": 1}}}
    ]

    mongo_results_category = query_mongo(mongo_db, category_pipeline_mongo)
    mongo_results_warehouse = query_mongo(mongo_db, warehouse_pipeline_mongo)

    save_results_to_txt(pg_results_category, "postgres_category_results.txt")
    save_results_to_txt(pg_results_warehouse, "postgres_warehouse_results.txt")
    save_results_to_txt(mongo_results_category, "mongo_category_results.txt")
    save_results_to_txt(mongo_results_warehouse, "mongo_warehouse_results.txt")

    generate_graph(pg_results_category, "Productos por Categoría (PostgreSQL)", "pg_category_chart.png")
    generate_graph(mongo_results_category, "Productos por Categoría (MongoDB)", "mongo_category_chart.png")

    print("Consultas y evidencias generadas exitosamente.")
except Exception as e:
    print("Error:", e)
finally:
    if postgres_conn:
        postgres_conn.close()
