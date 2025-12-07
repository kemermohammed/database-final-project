from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()  # Load your .env variables

# Connect to university PostgreSQL
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}")

def execute(query):
    with engine.connect() as conn:
        try:
            conn.execute(text(query))
            conn.commit()
        except IntegrityError:
            print("Already exists or integrity error")

# --- Create schema ---
execute("CREATE SCHEMA IF NOT EXISTS online_retail;")
execute("SET search_path = 'online_retail';")

# --- Create tables ---
execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id   INT PRIMARY KEY,
    city          VARCHAR(150) NOT NULL,
    age           INT NOT NULL,
    gender        VARCHAR(10)
    
);
""")

execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE
);
""")

execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0)
);
""")
execute("DROP TABLE IF EXISTS online_retail.orders CASCADE;")
execute(
    """CREATE TABLE IF NOT EXISTS orders (
    
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE NOT NULL,
    payment_method VARCHAR(50),
    total_amount DECIMAL(10,2), CHECK (total_amount >= 0)
);""")

execute("DROP TABLE IF EXISTS online_retail.order_product CASCADE;")
execute("""
CREATE TABLE IF NOT EXISTS order_product (
    order_product_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    price DECIMAL(10,2),
    review_score INT
);
""")



print("All tables created successfully!")


df = pd.read_sql("SELECT * FROM online_retail.orders LIMIT 0;", engine)
print("\nColumns in 'orders' table:", df.columns.tolist())
df = pd.read_sql("SELECT * FROM online_retail.order_product LIMIT 0;", engine)
print("\nColumns in 'orders' table:", df.columns.tolist())