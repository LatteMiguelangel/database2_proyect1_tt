import json
from connection import db

# -------------------------------
# 1. Atlas Search (fuzzy search)
# -------------------------------
def fuzzy_search_products(query: str, limit: int = 10):
    pipeline = [
        {
            "$search": {
                "text": {
                    "query": query,
                    "path": ["Product Name", "Product Description"],
                    "fuzzy": {"maxEdits": 2, "prefixLength": 1}
                }
            }
        },
        {"$limit": limit}
    ]
    return list(db["Products"].aggregate(pipeline))


# -------------------------------
# 2. Crear índices tradicionales
# -------------------------------
def create_indexes():
    # Orders
    db["Orders"].create_index([("Order Date", 1)])
    db["Orders"].create_index([("Customer ID", 1)])
    db["Orders"].create_index([("Customer ID", 1), ("Order Date", 1)])
    db["Orders"].create_index([("Product ID", 1)])

    # Products
    db["Products"].create_index([("Product ID", 1)], unique=True)
    db["Products"].create_index([("Sub-Category", 1), ("Product Name", 1)])

    print("Indexes created successfully.")


# -------------------------------
# 3. Explain Plan comparativo
# -------------------------------
def query_orders(customer_id: str, start_date: str, end_date: str):
    return {
        "Customer ID": customer_id,
        "Order Date": {"$gte": start_date, "$lte": end_date}
    }

def run_explain(collection_name: str, query: dict):
    # Ejecuta el comando explain sobre un find
    return db.command("explain", {
        "find": collection_name,
        "filter": query
    })

def summarize_explain(explain: dict):
    stats = explain.get("executionStats", {})
    return {
        "executionTimeMillis": stats.get("executionTimeMillis"),
        "totalDocsExamined": stats.get("totalDocsExamined"),
        "totalKeysExamined": stats.get("totalKeysExamined"),
        "winningPlanStage": explain.get("queryPlanner", {}).get("winningPlan", {}).get("stage"),
        "indexName": explain.get("queryPlanner", {}).get("winningPlan", {}).get("inputStage", {}).get("indexName")
    }


# -------------------------------
# 4. Main demo
# -------------------------------
if __name__ == "__main__":
    # 1. Prueba búsqueda fuzzy
    print("=== Fuzzy Search Example ===")
    results = fuzzy_search_products("plantronics cs510")
    for r in results:
        print(r)

    # 2. Crear índices
    print("\n=== Creating Indexes ===")
    create_indexes()

    # 3. Explain antes/después
    print("\n=== Explain Plan Comparison ===")
    q = query_orders("RH-19495", "2012-01-01", "2012-12-31")

    before = run_explain("Orders", q)
    print("Before:", summarize_explain(before))
    with open("explain_before.json", "w") as f:
        json.dump(before, f, indent=2)

    # (Después de crear índices, vuelve a correr el mismo query)
    after = run_explain("Orders", q)
    print("After:", summarize_explain(after))
    with open("explain_after.json", "w") as f:
        json.dump(after, f, indent=2)