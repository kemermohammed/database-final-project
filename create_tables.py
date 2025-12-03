from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

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
    customer_id INT PRIMARY KEY,
    city VARCHAR(100),
    age INT,
    gender CHAR(10)
);
""")

execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(100)
);
""")

execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2)
);
""")

execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    payment_method VARCHAR(50),
    total_amount DECIMAL(10,2)
);
""")

execute("""
CREATE TABLE IF NOT EXISTS order_product (
    order_product_id INT PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    price DECIMAL(10,2)
);
""")

execute("""
CREATE TABLE IF NOT EXISTS reviews (
    review_id INT PRIMARY KEY,
    order_product_id INT REFERENCES order_product(order_product_id),
    review_score INT
);
""")

print("All tables created successfully!")
