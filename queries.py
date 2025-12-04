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

# Example query
df = query("SELECT * FROM online_retail.customers LIMIT 5;")
print(df)
df = query("SELECT * FROM online_retail.categories LIMIT 5;")
print(df)
