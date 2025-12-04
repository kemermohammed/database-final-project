import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
user = os.getenv("USERNAME_DB")
password = os.getenv("PASSWORD")
db = os.getenv("NAME_DB")

# Connect to PostgreSQL
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@postgresql-edu.in.centralelille.fr:5432/{db}")

# Define execute function
def execute(query):
    with engine.begin() as conn:
        try:
            conn.execute(text(query))
        except IntegrityError as e:
            print("Integrity error:", e)

# Step 1: Truncate products table
##TRUNCATE TABLE online_retail.products RESTART IDENTITY CASCADE;
execute("TRUNCATE TABLE online_retail.reviews RESTART IDENTITY CASCADE;")  

# Step 2: Load products CSV
review_df = pd.read_csv("reviews.csv")


# Step 3: Insert into products table
review_df.to_sql(
    "reviews",
    engine,
    schema="online_retail",
    if_exists="append",
    index=False
)

print("Reviews table populated successfully!")
