import json
import pandas as pd

input_json = "./Global_Superstore2.json"
out_orders = "./orders.json"
out_customers = "./customers.json"
out_products = "./products.json"

# Leer JSON original
df = pd.read_json(input_json)
df.columns = [c.strip() for c in df.columns]

# --- 1) Orders: objetos planos con referencias a Customer ID y Product ID
orders_fields = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Sales", "Quantity", "Discount", "Profit", "Shipping Cost", "Order Priority",
    "Customer ID", "Product ID"
]

orders_list = []
for _, row in df.iterrows():
    order = {f: (row.get(f) if f in df.columns else None) for f in orders_fields}
    orders_list.append(order)

# --- 2) Customers: únicos por Customer ID, objeto plano con subdocumento Address
customers_map = {}
cust_fields_top = ["Customer ID", "Customer Name", "Segment", "Market"]
addr_fields = ["City", "State", "Country", "Postal Code", "Region"]

for _, row in df.iterrows():
    cid = row.get("Customer ID")
    if pd.isna(cid):
        continue
    if cid not in customers_map:
        cust = {k: row.get(k) for k in cust_fields_top if k in df.columns}
        address = {k: row.get(k) for k in addr_fields if k in df.columns}
        # Opcional: normalizar Postal Code a int si es .0 (evita 10024.0)
        pc = address.get("Postal Code")
        if isinstance(pc, float) and pc.is_integer():
            address["Postal Code"] = int(pc)
        cust["Address"] = address
        customers_map[cid] = cust

customers_list = list(customers_map.values())

# --- 3) Products: únicos por Product ID, objetos planos
products_map = {}
prod_fields = ["Product ID", "Category", "Sub-Category", "Product Name"]

for _, row in df.iterrows():
    pid = row.get("Product ID")
    if pd.isna(pid):
        continue
    if pid not in products_map:
        prod = {k: row.get(k) for k in prod_fields if k in df.columns}
        products_map[pid] = prod

products_list = list(products_map.values())

# --- 4) Guardar archivos (jsonArray) sin envoltorios
with open(out_orders, "w", encoding="latin-1") as f:
    json.dump(orders_list, f, ensure_ascii=False, indent=2)

with open(out_customers, "w", encoding="latin-1") as f:
    json.dump(customers_list, f, ensure_ascii=False, indent=2)

with open(out_products, "w", encoding="latin-1") as f:
    json.dump(products_list, f, ensure_ascii=False, indent=2)

print(" -", out_orders, "->", len(orders_list), "registros")
print(" -", out_customers, "->", len(customers_list), "clientes únicos")
print(" -", out_products, "->", len(products_list), "productos únicos")