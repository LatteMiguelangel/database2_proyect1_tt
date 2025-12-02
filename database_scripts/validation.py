from database_scripts.connection import db

# --- Orders ---
orders_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Order ID", "Customer ID", "Product ID"],
        "properties": {
            "Order ID": {"bsonType": "string"},
            "Row ID": {"bsonType": ["int", "long"]},
            "Order Date": {
                "bsonType": "string",
                "pattern": r"^\d{4}-\d{2}-\d{2}$",
                "description": "Formato YYYY-MM-DD"
            },
            "Ship Date": {
                "bsonType": "string",
                "pattern": r"^\d{4}-\d{2}-\d{2}$",
                "description": "Formato YYYY-MM-DD"
            },
            "Ship Mode": {"bsonType": "string", "description": "String"},
            "Sales": {"bsonType": "double", "minimum": 0,"description": "String"},
            "Quantity": {"bsonType": "int", "description": "String"},
            "Discount": {"bsonType": "double", "description": "String"},
            "Profit": {"bsonType": "double", "description": "String"},
            "Shipping Cost": {"bsonType": "double", "description": "String"},
            "Order Priority": {"bsonType": "string", "description": "String"},
            "Customer ID": {"bsonType": "string", "description": "String"},
            "Product ID": {"bsonType": "string", "description": "String"}
        }
    }
}

#db.create_collection("Orders", validator=orders_validator, validationLevel="strict")

# --- Customers ---
customers_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Customer ID", "Customer Name"],
        "properties": {
            "Customer ID": {"bsonType": "string", "description": "String"},
            "Customer Name": {"bsonType": "string", "description": "String"},
            "Segment": {"bsonType": "string", "description": "String"},
            "Market": {"bsonType": "string", "description": "String"},
            "Address": {
                "bsonType": "object",
                "properties": {
                    "City": {"bsonType": "string", "description": "String"},
                    "State": {"bsonType": "string", "description": "String"},
                    "Country": {"bsonType": "string", "description": "String"},
                    "Postal Code": {"bsonType": ["string", "int", "long", "double"], "description": "String"},
                    "Region": {"bsonType": "string", "description": "String"}
                }
            },
        }
    }
}

#db.create_collection("Customers", validator=customers_validator, validationLevel="strict")

# --- Products ---
products_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["Product ID", "Category", "Product Name"],
        "properties": {
            "Product ID": {"bsonType": "string", "description": "String"},
            "Category": {"bsonType": "string", "description": "String"},
            "Sub-Category": {"bsonType": "string", "description": "String"},
            "Product Name": {"bsonType": "string", "description": "String"}
        }
    }
}

#db.create_collection("Products", validator=products_validator, validationLevel="strict")