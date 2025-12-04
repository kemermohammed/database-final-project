import pandas as pd

# Load CSV
df = pd.read_csv("order_product.csv")

# Preview first few rows
#print(products_df.head())
# Check for missing values
# Check if there are duplicates
print("Total duplicate rows:", df.duplicated().sum())
print(df[df.duplicated()])
print(df.isnull().sum())