import pandas as pd
from pathlib import Path

df = pd.read_csv("data/raw/order_items.csv")

output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

df.to_csv(output_dir / "order_items.csv", index=False)

print("Order items prepared:", len(df))
print("Saved to data/processed/order_items.csv")