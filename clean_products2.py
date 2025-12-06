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
#drop duplicates
products_df = products_df.drop_duplicates(subset="product_id", keep="first")
# check duplicates again

# Save cleaned CSV
products_df.to_csv("cleaned_products3.csv", index=False)
print("Cleaned products CSV saved as cleaned_products.csv") 