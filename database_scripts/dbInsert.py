from database_scripts.connection import db
import json

ORDERS_JSON = "./data/processed/orders.json"
PRODUCTS_JSON = "./data/processed/products.json"
CUSTOMERS_JSON = "./data/processed/customers.json"


def insert_customer(productId, category, subCategory, productName):
    #funcion de prueba
    try:
        result = db["Products"].insert_one({
            "Product ID": productId,
            "Category": category,
            "Sub-Category": subCategory,
            "Product Name": productName,
        })
    except Exception as e:
        print(e)

def insert_all_customers():
    try:
        with open(CUSTOMERS_JSON, "r", encoding="latin-1") as f:
            data = json.load(f)
            result = db["Customers"].insert_many(data)
    except Exception as e:
        print(e)

def insert_all_orders():
    try:
        with open(ORDERS_JSON, "r", encoding="latin-1") as f:
            data = json.load(f)
            result = db["Orders"].insert_many(data)
    except Exception as e:
        print(e)

def insert_all_products():
    try:
        with open(PRODUCTS_JSON, "r", encoding="latin-1") as f:
            data = json.load(f)
            result = db["Products"].insert_many(data)
    except Exception as e:
        print(e)

insert_all_customers()
insert_all_orders()
insert_all_products()