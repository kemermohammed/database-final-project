import pandas as pd

# Load dataset
df = pd.read_csv("synthetic_online_retail_data.csv")

print("\n--- Raw Data Info ---")
print(df.info())
print("\n--- Missing values per column ---")
print(df.isnull().sum())

# 1. Remove duplicate rows (entire row duplicates)
df = df.drop_duplicates()

# 2. Strip whitespace from all text/object columns
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

# 3. Standardize category names
category_map = {
    "Electronics": "Electronics",
    "electronics": "Electronics",
    "Fashion": "Fashion",
    "Home & Living": "Home & Living",
    "Books & Stationery": "Books & Stationery",
    "Sports & Outdoors": "Sports & Outdoors"
}
df["category_name"] = df["category_name"].replace(category_map)

# 4. Standardize payment_method and city
df["payment_method"] = df["payment_method"].str.title()
df["city"] = df["city"].str.title()

# 5. Convert price and quantity to numeric
df["price"] = pd.to_numeric(df["price"], errors='coerce')
df["quantity"] = pd.to_numeric(df["quantity"], errors='coerce')

# 6. Remove rows with missing essential fields
df = df.dropna(subset=["customer_id", "product_id", "order_date"])

# 7. Convert order_date to datetime
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
df = df.dropna(subset=["order_date"])

# 8. Handle missing review_score and gender
df["review_score"] = df["review_score"].fillna(0)
df["gender"] = df["gender"].fillna("Unknown")

# 9. Filter unrealistic values
df = df[(df["age"] >= 10) & (df["age"] <= 100)]
df = df[(df["price"] >= 10) & (df["price"] <= 500)]
df = df[(df["quantity"] >= 1) & (df["quantity"] <= 5)]

# 10. Convert IDs to string (safer for DB)
df["customer_id"] = df["customer_id"].astype(str)
df["product_id"] = df["product_id"].astype(str)
df["category_id"] = df["category_id"].astype(str)

# 11. Remove duplicates based on meaningful order info
df = df.drop_duplicates(subset=["customer_id", "order_date", "product_id"])

# 12. Create derived columns
df["total_amount"] = df["quantity"] * df["price"]
df["order_year"] = df["order_date"].dt.year
df["order_month"] = df["order_date"].dt.month

# 13. Convert categorical columns to 'category' dtype
cat_cols = ["category_name", "payment_method", "gender", "city"]
for col in cat_cols:
    df[col] = df[col].astype("category")

# 14. Reorder columns for readability
cols = ["customer_id","order_date","product_id","category_id","category_name","product_name",
        "quantity","price","payment_method","city","review_score","gender","age",
        "total_amount","order_year","order_month"]
df = df[cols]

print("\n--- Cleaned Data Info ---")
print(df.info())
print("\n--- Missing values per column (after cleaning) ---")
print(df.isnull().sum())

# Save cleaned file
output_file = "cleaned_retail_data_final.csv"
df.to_csv(output_file, index=False)
print(f"\nCleaned dataset saved as: {output_file}")
