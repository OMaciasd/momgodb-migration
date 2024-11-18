# Obtener productos enviados desde una bodega específica
warehouse_name = "Central Warehouse"  # Cambiar por la bodega deseada
warehouse_id = db.warehouse.find_one({"name": warehouse_name})["_id"]

products = db.orders.aggregate([
    {"$unwind": "$items"},
    {"$lookup": {
        "from": "inventories",
        "localField": "items.product_id",
        "foreignField": "product_id",
        "as": "inventory_details"
    }},
    {"$unwind": "$inventory_details"},
    {"$match": {"inventory_details.warehouse_id": warehouse_id}},
    {"$project": {
        "order_id": 1,
        "items.product_id": 1,
        "items.quantity": 1,
        "inventory_details.warehouse_id": 1
    }}
])
for product in products:
    print(product)
