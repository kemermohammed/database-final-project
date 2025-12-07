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

# --- Create product tables ---




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






print("order_Product created successfully!")


df = pd.read_sql("SELECT * FROM online_retail.order_product LIMIT 0;", engine)
print("\nColumns in 'product' table:", df.columns.tolist())
