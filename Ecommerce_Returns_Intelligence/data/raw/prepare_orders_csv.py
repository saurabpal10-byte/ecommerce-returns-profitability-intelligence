
import pandas as pd
from pathlib import Path

input_file = Path("data/raw/orders.csv")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

# Convert order_date from DD-MM-YYYY to YYYY-MM-DD
df["order_date"] = pd.to_datetime(
    df["order_date"],
    format="%d-%m-%Y",
    errors="coerce"
).dt.strftime("%Y-%m-%d")

# Keep order_month in YYYY-MM format
df["order_month"] = df["order_month"].astype("string")

# Preserve missing delivery_days as blank values
df["delivery_days"] = pd.to_numeric(
    df["delivery_days"], errors="coerce"
).astype("Int64")

output_file = output_dir / "orders.csv"
df.to_csv(output_file, index=False)

print("Orders CSV prepared successfully.")
print("Total records:", len(df))
print("Missing delivery days:", df["delivery_days"].isna().sum())
print("Saved to:", output_file)
