# Load the cleaned dataset
import pandas as pd
import numpy as np

df = pd.read_csv("cleaned_retail_data_final.csv")
df['order_id'] = range(1, len(df)+1)

# Shipping table
df['shipping_id'] = range(1, len(df)+1)
df['shipping_date'] = pd.to_datetime(df['order_date']) + pd.to_timedelta(np.random.randint(1, 8, size=len(df)), unit='d')
df['shipping_status'] = np.random.choice(['Pending', 'Shipped', 'Delivered', 'Returned'], size=len(df))

shipping_table = df[['shipping_id', 'order_id', 'shipping_date', 'shipping_status']]
shipping_table.to_csv("shipping_table.csv", index=False)
print("Shipping table saved as shipping_table.csv")
# Discount table
df['discount_id'] = range(1, len(df)+1)
df['discount_amount'] = df['total_amount'] * np.random.choice([0, 0.05, 0.1, 0.15, 0.2], size=len(df))
df['discount_type'] = np.random.choice(['None', 'Seasonal', 'Clearance', 'Member'], size=len(df))

discount_table = df[['discount_id', 'order_id', 'discount_amount', 'discount_type']]
discount_table.to_csv("discount_table.csv", index=False)
print("Discount table saved as discount_table.csv")

df.to_csv("cleaned_retail_data_with_ids.csv", index=False)
print("Main dataset updated with shipping_id and discount_id")
