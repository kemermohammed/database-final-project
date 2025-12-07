import pandas as pd

# Load the dataset
df = pd.read_csv("synthetic_online_retail_data_realistic.csv")

# Clean gender and age
df['gender'] = df['gender'].apply(lambda x: x if str(x) in ['M', 'F'] else 'Null')
df['age'] = df['age'].apply(lambda x: x if 18 <= x <= 75 else 'Null')
df['review_score'] = df['review_score'].apply(lambda x: x if 1 <= x <= 5 else 'Null')

# Create customers table (unique rows only)
customers = df[['customer_id', 'city', 'age', 'gender']].drop_duplicates()
customers.to_csv("customers2.csv", index=False)

# Filter df to only include customer_ids present in customers
df = df[df['customer_id'].isin(customers['customer_id'])]

# Products table
products = df[['product_id', 'product_name', 'category_id', 'price']].drop_duplicates()
products.to_csv("products3.csv", index=False)

# Orders table
orders_total = df.groupby('order_id').apply(
    lambda x: pd.Series({
        'order_id': x['order_id'].iloc[0],
        'customer_id': x['customer_id'].iloc[0],
        'order_date': x['order_date'].iloc[0],
        'payment_method': x['payment_method'].iloc[0],
        'total_amount': (x['quantity'] * x['price']).sum()  
    }),
    include_groups=False
).reset_index()
orders_total.to_csv("orders2.csv", index=False)

# Load cleaned products
products_df = pd.read_csv("cleaned_products3.csv")
valid_product_ids = products_df['product_id'].unique()

# Filter order_product to include only valid product_ids
order_product = df[df['product_id'].isin(valid_product_ids)][['order_id', 'product_id', 'quantity', 'price', 'review_score']]
order_product.to_csv("order_product2.csv", index=False)
