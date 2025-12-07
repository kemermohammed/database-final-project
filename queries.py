from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}")

def query(q):
    with engine.connect() as conn:
        return pd.read_sql_query(text(q), conn)

# Example queries
print("Customers table:")
df = query("SELECT * FROM online_retail.customers LIMIT 5;")
print(df)

print("\nCategories table:")
df = query("SELECT * FROM online_retail.categories LIMIT 5;")
print(df)

print("\nOrders table:")
df = query("SELECT * FROM online_retail.orders LIMIT 5;")
print(df)

print("\nSpecific Product (product_id=266):")
df = query("SELECT * FROM online_retail.products WHERE product_id=266;")
print(df)

print("\nTotal products:")
df = query("SELECT count(*) FROM online_retail.products;")
print(df)

print("\nTotal order_product entries:")
df = query("SELECT count(*) FROM online_retail.order_product;")
print(df)

print("\nTotal orders per customer:")
df = query("""
SELECT c.customer_id, c.city, COUNT(o.order_id) AS total_orders
FROM online_retail.customers c
LEFT JOIN online_retail.orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.city
ORDER BY total_orders DESC;
""")
print(df)

print("\nTotal revenue per customer:")
df = query("""
SELECT c.customer_id, c.city, SUM(o.total_amount) AS total_revenue
FROM online_retail.customers c
LEFT JOIN online_retail.orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.city
ORDER BY total_revenue DESC;
""")
print(df)

print("\nTop 10 best-selling products by quantity:")
df = query("""
SELECT p.product_id, p.product_name, SUM(op.quantity) AS total_quantity_sold
FROM online_retail.products p
JOIN online_retail.order_product op
ON p.product_id = op.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 10;
""")
print(df)

print("\nTop 10 highest revenue products:")
df = query("""
SELECT p.product_id, p.product_name, SUM(op.quantity * op.price) AS revenue
FROM online_retail.products p
JOIN online_retail.order_product op
ON p.product_id = op.product_id
GROUP BY p.product_id, p.product_name
ORDER BY revenue DESC
LIMIT 10;
""")
print(df)

print("\nOrders per payment method:")
df = query("""
SELECT payment_method, COUNT(order_id) AS total_orders
FROM online_retail.orders
GROUP BY payment_method
ORDER BY total_orders DESC;
""")
print(df)

print("\nMonthly revenue trends:")
df = query("""
SELECT DATE_TRUNC('month', order_date) AS month, SUM(total_amount) AS monthly_revenue
FROM online_retail.orders
GROUP BY month
ORDER BY month;
""")
print(df)

