# pipelines.py
from connection import db

def orders_sales_by_category_month(start_date: str, end_date: str):
    pipeline = [
        {"$match": {
            "$expr": {
                "$and": [
                    {"$gte": [{"$dateFromString": {"dateString": "$Order Date"}}, {"$dateFromString": {"dateString": start_date}}]},
                    {"$lte": [{"$dateFromString": {"dateString": "$Order Date"}}, {"$dateFromString": {"dateString": end_date}}]}
                ]
            }
        }},
        {"$addFields": {"orderMonth": {"$dateToString": {"format": "%Y-%m", "date": {"$dateFromString": {"dateString": "$Order Date"}}}}}},
        {"$lookup": {"from": "Products", "localField": "Product ID", "foreignField": "Product ID", "as": "product"}},
        {"$unwind": {"path": "$product", "preserveNullAndEmptyArrays": False}},
        {"$group": {
            "_id": {"category": "$product.Category", "month": "$orderMonth"},
            "totalSales": {"$sum": "$Sales"},
            "orderCount": {"$sum": 1}
        }},
        {"$project": {"_id": 0, "category": "$_id.category", "month": "$_id.month", "totalSales": 1, "orderCount": 1}},
        {"$sort": {"month": 1, "category": 1}}
    ]
    return list(db["Orders"].aggregate(pipeline))


def customers_top_by_orders(limit: int = 10):
    """
    Top N clientes por número de órdenes (global).
    Retorna: customerId, customerName (si existe), orderCount, totalSales
    """
    pipeline = [
        {"$group": {"_id": "$Customer ID", "orderCount": {"$sum": 1}, "totalSales": {"$sum": "$Sales"}}},
        {"$sort": {"orderCount": -1, "totalSales": -1}},
        {"$limit": limit},
        {"$lookup": {"from": "Customers", "localField": "_id", "foreignField": "Customer ID", "as": "customer"}},
        {"$unwind": {"path": "$customer", "preserveNullAndEmptyArrays": True}},
        {"$project": {"_id": 0, "customerId": "$_id", "customerName": "$customer.Customer Name", "orderCount": 1, "totalSales": 1}}
    ]
    return list(db["Orders"].aggregate(pipeline))


def customer_top_by_orders_in_range(start_date: str, end_date: str):
    """
    Cliente que más órdenes hizo en un rango de fechas.
    Retorna un dict (vacío si no hay resultados): customerId, customerName, orderCount, totalSales
    """
    pipeline = [
        {"$match": {
            "$expr": {
                "$and": [
                    {"$gte": [{"$dateFromString": {"dateString": "$Order Date"}}, {"$dateFromString": {"dateString": start_date}}]},
                    {"$lte": [{"$dateFromString": {"dateString": "$Order Date"}}, {"$dateFromString": {"dateString": end_date}}]}
                ]
            }
        }},
        {"$group": {"_id": "$Customer ID", "orderCount": {"$sum": 1}, "totalSales": {"$sum": "$Sales"}}},
        {"$sort": {"orderCount": -1, "totalSales": -1}},
        {"$limit": 1},
        {"$lookup": {"from": "Customers", "localField": "_id", "foreignField": "Customer ID", "as": "customer"}},
        {"$unwind": {"path": "$customer", "preserveNullAndEmptyArrays": True}},
        {"$project": {"_id": 0, "customerId": "$_id", "customerName": "$customer.Customer Name", "orderCount": 1, "totalSales": 1}}
    ]
    res = list(db["Orders"].aggregate(pipeline))
    return res[0] if res else {}


def products_bucket_by_price_by_subcategory():
    """
    Para cada Sub-Category:
      - obtiene precio por producto (si Products tiene campo de precio lo usa; si no, calcula unitPrice desde Orders: Sales/Quantity promedio por Product ID)
      - calcula avgPrice por Sub-Category
      - ratio = price / avgPrice
      - clasifica: ratio <= 0.3 -> low; 0.3 < ratio <= 0.6 -> medium; ratio > 0.6 -> high
    Retorna lista de dicts por subCategory con: subCategory, avgPrice, counts, sampleProducts
    """
    # Detectar campo de precio en Products
    sample = db["Products"].find_one() or {}
    price_field = None
    for f in ["Price", "Unit Price", "UnitPrice", "List Price", "PriceUSD"]:
        if f in sample:
            price_field = f
            break

    if price_field:
        # Hay campo de precio en Products: calcular avg por subcategory y clasificar
        pipeline = [
            {"$match": {price_field: {"$exists": True, "$ne": None}}},
            {"$group": {"_id": "$Sub-Category", "avgPrice": {"$avg": f"${price_field}"}}},
            {"$lookup": {"from": "Products", "localField": "_id", "foreignField": "Sub-Category", "as": "products"}},
            {"$unwind": {"path": "$products", "preserveNullAndEmptyArrays": False}},
            {"$project": {
                "subCategory": "$_id",
                "avgPrice": 1,
                "productId": "$products.Product ID",
                "productName": "$products.Product Name",
                "price": f"$products.{price_field}"
            }},
            {"$addFields": {"ratio": {"$cond": [{"$gt": ["$avgPrice", 0]}, {"$divide": ["$price", "$avgPrice"]}, None]}}},
            {"$addFields": {
                "priceCategory": {
                    "$switch": {
                        "branches": [
                            {"case": {"$lte": ["$ratio", 0.3]}, "then": "low"},
                            {"case": {"$and": [{"$gt": ["$ratio", 0.3]}, {"$lte": ["$ratio", 0.6]}]}, "then": "medium"}
                        ],
                        "default": "high"
                    }
                }
            }},
            {"$group": {
                "_id": "$subCategory",
                "avgPrice": {"$first": "$avgPrice"},
                "products": {"$push": {"productId": "$productId", "productName": "$productName", "price": "$price", "ratio": "$ratio", "priceCategory": "$priceCategory"}},
                "countLow": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "low"]}, 1, 0]}},
                "countMedium": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "medium"]}, 1, 0]}},
                "countHigh": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "high"]}, 1, 0]}}
            }},
            {"$project": {
                "_id": 0,
                "subCategory": "$_id",
                "avgPrice": 1,
                "counts": {"low": "$countLow", "medium": "$countMedium", "high": "$countHigh"},
                "sampleProducts": {"$slice": ["$products", 10]}
            }}
        ]
        return list(db["Products"].aggregate(pipeline))

    # Si no hay campo de precio en Products: calcular unitPrice desde Orders y unir con Products
    pipeline_orders = [
        {"$match": {"Quantity": {"$exists": True, "$gt": 0}, "Sales": {"$exists": True}}},
        {"$project": {"Product ID": 1, "unitPrice": {"$divide": ["$Sales", "$Quantity"]}}},
        {"$group": {"_id": "$Product ID", "avgUnitPrice": {"$avg": "$unitPrice"}}},
        {"$lookup": {"from": "Products", "localField": "_id", "foreignField": "Product ID", "as": "product"}},
        {"$unwind": {"path": "$product", "preserveNullAndEmptyArrays": False}},
        {"$project": {"productId": "$_id", "productName": "$product.Product Name", "subCategory": "$product.Sub-Category", "avgUnitPrice": 1}},
        {"$group": {"_id": "$subCategory", "avgPrice": {"$avg": "$avgUnitPrice"}, "products": {"$push": {"productId": "$productId", "productName": "$productName", "price": "$avgUnitPrice"}}}},
        {"$unwind": {"path": "$products", "preserveNullAndEmptyArrays": False}},
        {"$project": {
            "subCategory": "$_id",
            "avgPrice": 1,
            "productId": "$products.productId",
            "productName": "$products.productName",
            "price": "$products.price"
        }},
        {"$addFields": {"ratio": {"$cond": [{"$gt": ["$avgPrice", 0]}, {"$divide": ["$price", "$avgPrice"]}, None]}}},
        {"$addFields": {
            "priceCategory": {
                "$switch": {
                    "branches": [
                        {"case": {"$lte": ["$ratio", 0.3]}, "then": "low"},
                        {"case": {"$and": [{"$gt": ["$ratio", 0.3]}, {"$lte": ["$ratio", 0.6]}]}, "then": "medium"}
                    ],
                    "default": "high"
                }
            }
        }},
        {"$group": {
            "_id": "$subCategory",
            "avgPrice": {"$first": "$avgPrice"},
            "products": {"$push": {"productId": "$productId", "productName": "$productName", "price": "$price", "ratio": "$ratio", "priceCategory": "$priceCategory"}},
            "countLow": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "low"]}, 1, 0]}},
            "countMedium": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "medium"]}, 1, 0]}},
            "countHigh": {"$sum": {"$cond": [{"$eq": ["$priceCategory", "high"]}, 1, 0]}}
        }},
        {"$project": {
            "_id": 0,
            "subCategory": "$_id",
            "avgPrice": 1,
            "counts": {"low": "$countLow", "medium": "$countMedium", "high": "$countHigh"},
            "sampleProducts": {"$slice": ["$products", 10]}
        }}
    ]
    return list(db["Orders"].aggregate(pipeline_orders))


# helper
def available_collections():
    return db.list_collection_names()


if __name__ == "__main__":
    print("Collections:", available_collections())

    print("\n--- orders_sales_by_category_month ---")
    for r in orders_sales_by_category_month("2012-01-01", "2012-12-31")[:10]:
        print(r)

    print("\n--- customers_top_by_orders ---")
    for r in customers_top_by_orders(limit=10):
        print(r)

    print("\n--- customer_top_by_orders_in_range ---")
    print(customer_top_by_orders_in_range("2012-01-01", "2012-12-31"))

    print("\n--- products_bucket_by_price_by_subcategory ---")
    for r in products_bucket_by_price_by_subcategory():
        print(r)