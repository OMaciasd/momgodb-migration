category_name = "Electronics"
category_id = db.product_categories.find_one({"name": category_name})["_id"]

products = db.products.find({"category_id": category_id})
for product in products:
    print(product)
