from database_scripts.connection import db
import json

ORDERS_JSON = "./orders.json"
PRODUCTS_JSON = "./products.json"
CUSTOMERS_JSON = "./customers.json"


def insert_client(): #funcion de prueba
    try:
        result = db["Products"].insert_one({
            "Product ID": "IDPRUEBA",
            "Category": "A",
            "Sub-Category": "a",
            "Product Name": "Anuel AA",
        })
    except Exception as e:
        print(e)

def insert_all_clients():
    try:
        with open(CUSTOMERS_JSON, "r", encoding="latin-1") as f:
            data = json.load(f)
            result = db["Customers"].insert_many(data)
    except Exception as e:
        print(e)

insert_all_clients()