import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/products.csv")

df["launch_date"] = pd.to_datetime(
    df["launch_date"],
    format="%d-%m-%Y",
    errors="coerce"
).dt.strftime("%Y-%m-%d")

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "products.csv", index=False)

print("Products CSV prepared successfully.")
print("Total records:", len(df))
print("Saved to: data/processed/products.csv")