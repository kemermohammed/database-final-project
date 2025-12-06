import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}")

# Optional: truncate table first
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE online_retail.orders RESTART IDENTITY CASCADE;"))

# Load orders CSV
df_orders = pd.read_csv("orders.csv")

# Insert into database
df_orders.to_sql(
    "orders",
    engine,
    schema="online_retail",
    if_exists="append",
    index=False
)

# Verify first 5 rows
with engine.connect() as conn:
    print("\nOrders sample:")
    for row in conn.execute(text("SELECT * FROM online_retail.orders LIMIT 5;")):
        print(row)

print("\nOrders table populated successfully!")
df = pd.read_sql("SELECT COUNT(*) AS total_rows FROM online_retail.orders;", engine)
print("Total rows in products table:", df['total_rows'][0])
