db.orders.aggregate([
    {"$group": {"_id": "$status", "total_orders": {"$sum": 1}}}
])
