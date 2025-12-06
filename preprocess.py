import pandas as pd
import numpy as np




# Load the dataset
df = pd.read_csv("synthetic_online_retail_data_realistic.csv")

df['gender'] = df['gender'].apply(lambda x: x if str(x) in ['M', 'F'] else 'Null')
df['age'] = df['age'].apply(lambda x: x if 18 <= x <= 75 else 'Null')
df['review_score'] = df['review_score'].apply(lambda x: x if 1 <= x <= 5 else 'Null')
# Customers table
customers = df[['customer_id', 'city', 'age', 'gender']].drop_duplicates()

customers.to_csv("customers2.csv", index=False)

#Products table
products = df[['product_id', 'product_name', 'category_id', 'price']].drop_duplicates()
products.to_csv("products3.csv", index=False)

orders_total = df.groupby('order_id').apply(
    lambda x: pd.Series({
        'customer_id': x['customer_id'].iloc[0],
        'order_date': x['order_date'].iloc[0],
        'payment_method': x['payment_method'].iloc[0],
        'total_amount': (x['quantity'] * x['price']).sum()  
    
    }),
    include_groups=False
).reset_index()
orders_total = orders_total.drop(columns=['order_id'])

orders_total.to_csv("orders2.csv", index=False)
#df = df.reset_index(drop=True)
#df['order_product_id'] = df.index + 1

# Order_Product table
order_product = df[['order_id', 'product_id', 'quantity', 'price', 'review_score']]
order_product.to_csv("order_product2.csv", index=False)