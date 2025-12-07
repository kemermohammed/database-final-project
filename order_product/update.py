import pandas as pd

# Load the original order_product CSV
order_product = pd.read_csv("order_product2.csv")  # your CSV with columns: order_id, product_id, quantity, price, review_score

# Remove old order_id (if you want to assign new serial numbers)
if 'order_id' in order_product.columns:
    order_product = order_product.drop(columns=['order_id'])

# Assign new order_id starting from 1000, sequentially grouped by "logical order"
# Here, assuming each unique combination of customer/order creates a new order
# If you don't have customer info, we just assign sequentially based on rows
num_rows = len(order_product)
order_product['order_id'] = range(1000, 1000 + num_rows)

# Reorder columns
order_product = order_product[['order_id', 'product_id', 'quantity', 'price', 'review_score']]

# Save updated CSV
order_product.to_csv("order_product_updated.csv", index=False)
print("Updated order_product CSV saved as 'order_product_updated.csv'")
