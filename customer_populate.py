import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

# ------------------------
# Load environment variables
# ------------------------
load_dotenv()
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")

# ------------------------
# Connect to PostgreSQL
# ------------------------
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}")

# ------------------------
# Define execute function
# ------------------------
def execute(query):
    with engine.begin() as conn:  # engine.begin handles commit automatically
        try:
            conn.execute(text(query))
        except IntegrityError as e:
            print("Integrity error:", e)

# ------------------------
# Truncate table (optional, for fresh insert)
# ------------------------
execute("TRUNCATE TABLE online_retail.customers RESTART IDENTITY CASCADE;")

# ------------------------
# Load CSV
# ------------------------
customers_df = pd.read_csv("customers.csv")

# Replace "Null" with real None
customers_df['gender'] = customers_df['gender'].replace(["Null", "NULL", "null"], None)

# ------------------------
# Insert data
# ------------------------
customers_df.to_sql(
    "customers",
    engine,
    schema="online_retail",
    if_exists="append",
    index=False
)

print("Customers table populated successfully!")
