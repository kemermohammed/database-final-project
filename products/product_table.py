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



execute("DROP TABLE IF EXISTS online_retail.products CASCADE;")
execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category_id INT REFERENCES categories(category_id),
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0)
);
""")






print("Product created successfully!")


df = pd.read_sql("SELECT * FROM online_retail.products LIMIT 0;", engine)
print("\nColumns in 'product' table:", df.columns.tolist())
