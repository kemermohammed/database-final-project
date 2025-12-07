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
execute("TRUNCATE TABLE online_retail.order_product RESTART IDENTITY CASCADE;")

# ------------------------
# Load CSV
# ------------------------
orders_df = pd.read_csv("order_product2.csv")

orders_df['review_score'] = orders_df['review_score'].replace(["Null", "NULL", "null"], None)
# Convert review_score to integer (handle None or missing values)
orders_df["review_score"] = (
    orders_df["review_score"]
    .replace("None", None)      # optional if "None" exists
    .astype(float)              # convert "5.0" -> 5.0
    .round()                    # round if needed
    .astype("Int64")            # Pandas nullable integer
)

# ------------------------
# Insert data
# ------------------------
#orders_df.drop(columns=['order_id'], inplace=True)  # let PostgreSQL handle the ID
orders_df.to_sql(
    "order_product",
    engine,
    schema="online_retail",
    if_exists="append",
    index=False
)


print("orders table populated successfully!")
df = pd.read_sql("SELECT COUNT(*) AS total_rows FROM online_retail.order_product;", engine)
print("Total rows in products table:", df['total_rows'][0])

df = pd.read_sql("SELECT * FROM online_retail.order_product LIMIT 10;", engine)
print(df)
