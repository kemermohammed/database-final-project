import pandas as pd

# Load your CSV
df = pd.read_csv("orders2.csv")

# Assign auto-incrementing order_id starting from 1000
df.insert(0, 'order_id', range(1000, 1000 + len(df)))

# Save to a new CSV
df.to_csv("orders_with_id.csv", index=False)

print(df)
