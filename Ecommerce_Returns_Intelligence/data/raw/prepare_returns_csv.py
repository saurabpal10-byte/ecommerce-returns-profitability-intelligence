import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/returns.csv")

df["return_date"] = pd.to_datetime(
    df["return_date"],
    format="%d-%m-%Y",
    errors="coerce"
).dt.strftime("%Y-%m-%d")

df["return_month"] = df["return_month"].astype("string")

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "returns.csv", index=False)

print("Returns CSV prepared successfully.")
print("Total records:", len(df))
print("Saved to: data/processed/returns.csv")