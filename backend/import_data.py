import pandas as pd
import mysql.connector


# ==========================================
# 1. LOAD DATASET
# ==========================================

file_path = "dataset/Amazon.csv"

df = pd.read_csv(file_path)

print(f"Dataset loaded successfully: {len(df)} rows")


# ==========================================
# 2. CONNECT TO MYSQL
# ==========================================

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ecommerce_intelligence"
)

cursor = connection.cursor()

print("MySQL connected successfully!")


# ==========================================
# 3. FUNCTION FOR BATCH INSERT
# ==========================================

def insert_in_batches(cursor, connection, query, data, table_name):

    batch_size = 500
    total = len(data)

    for i in range(0, total, batch_size):

        batch = data[i:i + batch_size]

        cursor.executemany(query, batch)

        connection.commit()

        processed = min(i + batch_size, total)

        print(
            f"{table_name}: "
            f"{processed}/{total} processed"
        )


# ==========================================
# 4. INSERT CUSTOMERS
# ==========================================

print("\nInserting customers...")

customers = df[
    [
        "CustomerID",
        "CustomerName",
        "City",
        "State",
        "Country"
    ]
].drop_duplicates(subset=["CustomerID"])

customer_query = """
INSERT IGNORE INTO customers
(
    customer_id,
    customer_name,
    city,
    state,
    country
)
VALUES (%s, %s, %s, %s, %s)
"""

customer_data = [
    tuple(row)
    for row in customers.itertuples(
        index=False,
        name=None
    )
]

insert_in_batches(
    cursor,
    connection,
    customer_query,
    customer_data,
    "Customers"
)


# ==========================================
# 5. INSERT PRODUCTS
# ==========================================

print("\nInserting products...")

products = df[
    [
        "ProductID",
        "ProductName",
        "Category",
        "Brand"
    ]
].drop_duplicates(subset=["ProductID"])

product_query = """
INSERT IGNORE INTO products
(
    product_id,
    product_name,
    category,
    brand
)
VALUES (%s, %s, %s, %s)
"""

product_data = [
    tuple(row)
    for row in products.itertuples(
        index=False,
        name=None
    )
]

insert_in_batches(
    cursor,
    connection,
    product_query,
    product_data,
    "Products"
)


# ==========================================
# 6. INSERT SELLERS
# ==========================================

print("\nInserting sellers...")

sellers = df[
    ["SellerID"]
].drop_duplicates()

seller_query = """
INSERT IGNORE INTO sellers
(
    seller_id
)
VALUES (%s)
"""

seller_data = [
    tuple(row)
    for row in sellers.itertuples(
        index=False,
        name=None
    )
]

insert_in_batches(
    cursor,
    connection,
    seller_query,
    seller_data,
    "Sellers"
)


# ==========================================
# 7. INSERT ORDERS
# ==========================================

print("\nInserting orders...")

orders = df[
    [
        "OrderID",
        "OrderDate",
        "CustomerID",
        "SellerID",
        "PaymentMethod",
        "OrderStatus"
    ]
].drop_duplicates(subset=["OrderID"])


# Convert date strings to proper date format
orders["OrderDate"] = pd.to_datetime(
    orders["OrderDate"]
).dt.date


order_query = """
INSERT IGNORE INTO orders
(
    order_id,
    order_date,
    customer_id,
    seller_id,
    payment_method,
    order_status
)
VALUES (%s, %s, %s, %s, %s, %s)
"""

order_data = [
    tuple(row)
    for row in orders.itertuples(
        index=False,
        name=None
    )
]

insert_in_batches(
    cursor,
    connection,
    order_query,
    order_data,
    "Orders"
)


# ==========================================
# 8. INSERT ORDER ITEMS
# ==========================================

print("\nInserting order items...")

order_items = df[
    [
        "OrderID",
        "ProductID",
        "Quantity",
        "UnitPrice",
        "Discount",
        "Tax",
        "ShippingCost",
        "TotalAmount"
    ]
]

item_query = """
INSERT INTO order_items
(
    order_id,
    product_id,
    quantity,
    unit_price,
    discount,
    tax,
    shipping_cost,
    total_amount
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

item_data = [
    tuple(row)
    for row in order_items.itertuples(
        index=False,
        name=None
    )
]

insert_in_batches(
    cursor,
    connection,
    item_query,
    item_data,
    "Order Items"
)


# ==========================================
# 9. FINISH
# ==========================================

cursor.close()
connection.close()

print("\n===================================")
print("DATA IMPORT COMPLETED SUCCESSFULLY!")
print("===================================")