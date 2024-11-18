db.orders.find({"_id": "order_44"})

db.orders.update_one({"_id": "order_44"}, {"$set": {"status": "Shipped"}})

db.orders.find({"_id": "order_44"})
