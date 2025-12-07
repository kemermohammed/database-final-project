import pandas as pd

# Load CSV
products_df = pd.read_csv("products3.csv")

# Preview first few rows
print(products_df.head())
# Check for missing values
# Check if there are duplicates
duplicates = products_df[products_df.duplicated(subset="product_id", keep=False)]

if not duplicates.empty:
    print("Duplicate product_ids found:")
    print(duplicates)
else:
    print("No duplicates found.")

# Check duplicates
print(f"Duplicate rows: {products_df.duplicated().sum()}")  


# Load cleaned products
products_df = pd.read_csv("cleaned_products3.csv")
valid_product_ids = products_df['product_id'].unique()

# Filter order_product to include only valid product_ids
order_product = df[df['product_id'].isin(valid_product_ids)][['order_id', 'product_id', 'quantity', 'price', 'review_score']]
order_product.to_csv("order_product2.csv", index=False)
