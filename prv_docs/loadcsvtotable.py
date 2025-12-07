import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to PostgreSQL
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")

engine = create_engine(
    f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}"
)

# -------------------------------------------------------------------
# Helper function to load any CSV into a table
# -------------------------------------------------------------------
def load_table(schema, table, csv_path):
    print(f"\n--- Loading {table} ---")
    df = pd.read_csv(csv_path)
    df = df.drop(columns=["order_id"], errors="ignore")
    df = df.drop(columns=["order_product_id"], errors="ignore")

    # 1. Truncate table & reset SERIAL counters
    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {schema}.{table} RESTART IDENTITY CASCADE;"))
        print(f"✓ Truncated {table}")
    
    # 2. Insert data
    df.to_sql(
        table,
        engine,
        schema=schema,
        if_exists="append",
        index=False
    )
    print(f"✓ Loaded {len(df)} rows into {table}")

# -------------------------------------------------------------------
# Load data in correct foreign-key order
# -------------------------------------------------------------------
load_table("online_retail", "categories", "categories.csv")
#load_table("online_retail", "customers", "customers2.csv")
#load_table("online_retail", "products", "cleaned_products3.csv")
#load_table("online_retail", "orders", "orders2.csv")
load_table("online_retail", "order_product", "order_product2.csv")

print("\nAll tables loaded successfully!")
