import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv("synthetic_online_retail_data 2.csv")

# ----------------------------
# 1. Clean the dataset
# ----------------------------

# Drop rows with missing critical identifiers
df.dropna(subset=['customer_id', 'product_id', 'category_id', 'price'], inplace=True)

# Ensure quantity > 0
df = df[df['quantity'] > 0]

# Ensure age in range 18-75
df = df[(df['age'] >= 18) & (df['age'] <= 75)]

# Ensure review_score between 1-5 or NaN
df['review_score'] = df['review_score'].apply(lambda x: x if 1 <= x <= 5 else np.nan)

# ----------------------------
# 2. Generate surrogate keys
# ----------------------------

# Orders: group by customer_id and order_date (assume each unique date per customer is one order)
df['order_group'] = df.groupby(['customer_id', 'order_date']).ngroup()
df['order_id'] = df['order_group'] + 1  # start from 1

# Order_Product: each row is unique line item
df = df.reset_index(drop=True)
df['order_product_id'] = df.index + 1

# Reviews: use order_product_id
df['review_id'] = df.index + 1

# ----------------------------
# 3. Prepare separate tables
# ----------------------------

# Customers table
customers = df[['customer_id', 'city', 'age', 'gender']].drop_duplicates()

# Categories table
categories = df[['category_id', 'category_name']].drop_duplicates()

# Products table
products = df[['product_id', 'product_name', 'category_id', 'price']].drop_duplicates()

# Orders table: compute total_amount per order
orders_total = df.groupby('order_id').apply(
    lambda x: pd.Series({
        'customer_id': x['customer_id'].iloc[0],
        'order_date': x['order_date'].iloc[0],
        'payment_method': x['payment_method'].iloc[0],
        'total_amount': (x['quantity'] * x['price']).sum()
    })
).reset_index()

# Order_Product table
order_product = df[['order_product_id', 'order_id', 'product_id', 'quantity', 'price']]

# Reviews table (nullable review_score)
reviews = df[['review_id', 'order_product_id', 'review_score']]

# ----------------------------
# 4. Save tables as CSV
# ----------------------------
customers.to_csv("customers.csv", index=False)
categories.to_csv("categories.csv", index=False)
products.to_csv("products.csv", index=False)
orders_total.to_csv("orders.csv", index=False)
order_product.to_csv("order_product.csv", index=False)
reviews.to_csv("reviews.csv", index=False)

print("All tables generated and saved successfully!")
