import pandas as pd
import random
from datetime import datetime, timedelta

# Load your CSV
df = pd.read_csv("synthetic_online_retail_data 2.csv")

orders = []
order_id_counter = 1000

for _, customer_row in df.iterrows():
    customer_id = customer_row["customer_id"]
    city = customer_row["city"]
    age = customer_row["age"]
    gender = customer_row["gender"]
    
    # Random number of orders per customer
    num_orders = random.randint(1, 4)
    for _ in range(num_orders):
        order_id = order_id_counter
        order_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
        
        # Random number of products per order
        num_products = random.randint(1, 3)
        for _ in range(num_products):
            product_row = df.sample(1).iloc[0]
            orders.append({
                "customer_id": customer_id,
                "order_id": order_id,
                "order_date": order_date.strftime("%Y-%m-%d"),
                "product_id": product_row["product_id"],
                "category_id": product_row["category_id"],
                "category_name": product_row["category_name"],
                "product_name": product_row["product_name"],
                "quantity": random.randint(1,5),
                "price": product_row["price"],
                "payment_method": product_row["payment_method"],
                "city": city,
                "review_score": product_row["review_score"],
                "gender": gender,
                "age": age
            })
        order_id_counter += 1

df_realistic = pd.DataFrame(orders)
df_realistic.to_csv("synthetic_online_retail_data_realistic.csv", index=False)
