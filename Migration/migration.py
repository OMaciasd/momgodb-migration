from pymongo import MongoClient
import psycopg2

MONGO_URI = "mongodb://localhost:27017"
POSTGRES_CONFIG = {
    "host": "localhost",
    "database": "source_db",
    "user": "user",
    "password": "password"
}

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["POC_DB"]

pg_conn = psycopg2.connect(**POSTGRES_CONFIG)
pg_cursor = pg_conn.cursor()


def migrate_orders():
    pg_cursor.execute("SELECT * FROM orders;")
    orders = pg_cursor.fetchall()

    for order in orders:
        mongo_order = {
            "_id": f"order_{order[0]}",
            "customer_id": order[1],
            "order_date": order[2].isoformat(),
            "status": order[3],
            "items": [],
            "total": order[4]
        }

        pg_cursor.execute(
            "SELECT * FROM order_items WHERE order_id = %s;", (order[0],)
        )
        items = pg_cursor.fetchall()
        for item in items:
            mongo_order["items"].append({
                "product_id": f"prod_{item[1]}",
                "quantity": item[2],
                "price": item[3]
            })
        db.orders.insert_one(mongo_order)
    print("Orders migradas con éxito.")


def migrate_products():
    pg_cursor.execute("SELECT * FROM products;")
    products = pg_cursor.fetchall()

    for product in products:
        mongo_product = {
            "_id": f"prod_{product[0]}",
            "name": product[1],
            "category_id": f"cat_{product[2]}",
            "price": product[3],
            "inventory_id": f"inv_{product[4]}"
        }
        db.products.insert_one(mongo_product)
    print("Products migrados con éxito.")


def migrate_product_categories():
    pg_cursor.execute("SELECT * FROM product_categories;")
    categories = pg_cursor.fetchall()

    for category in categories:
        mongo_category = {
            "_id": f"cat_{category[0]}",
            "name": category[1],
            "description": category[2]
        }
        db.product_categories.insert_one(mongo_category)
    print("Product_Categories migradas con éxito.")


def migrate_inventories():
    pg_cursor.execute("SELECT * FROM inventories;")
    inventories = pg_cursor.fetchall()

    for inventory in inventories:
        mongo_inventory = {
            "_id": f"inv_{inventory[0]}",
            "warehouse_id": f"wh_{inventory[1]}",
            "product_id": f"prod_{inventory[2]}",
            "stock": inventory[3]
        }
        db.inventories.insert_one(mongo_inventory)
    print("Inventories migradas con éxito.")


def migrate_warehouses():
    pg_cursor.execute("SELECT * FROM warehouse;")
    warehouses = pg_cursor.fetchall()

    for warehouse in warehouses:
        mongo_warehouse = {
            "_id": f"wh_{warehouse[0]}",
            "name": warehouse[1],
            "location": warehouse[2]
        }
        db.warehouse.insert_one(mongo_warehouse)
    print("Warehouses migrados con éxito.")


def main():
    try:
        migrate_orders()
        migrate_products()
        migrate_product_categories()
        migrate_inventories()
        migrate_warehouses()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pg_cursor.close()
        pg_conn.close()
        mongo_client.close()
        print("Conexiones cerradas.")


if __name__ == "__main__":
    main()
