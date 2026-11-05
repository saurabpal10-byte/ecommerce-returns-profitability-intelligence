import pandas as pd
from pathlib import Path

input_file = Path("data/raw/customers.csv")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_file)

for column in ["signup_date", "first_order_date"]:
    df[column] = pd.to_datetime(
        df[column],
        format="%d-%m-%Y",
        errors="coerce"
    ).dt.strftime("%Y-%m-%d")

output_file = output_dir / "customers.csv"
df.to_csv(output_file, index=False)

print("Customer CSV prepared successfully.")
print("Total records:", len(df))
print("Saved to:", output_file)