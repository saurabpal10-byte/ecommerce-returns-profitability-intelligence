
from pathlib import Path
from contextlib import redirect_stdout
import pandas as pd
import numpy as np
import io
import traceback

# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "raw"
REPORT_DIR = BASE_DIR / "reports"
REPORT_PATH = REPORT_DIR / "data_audit_report.txt"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_csv(filename):
    path = DATA_DIR / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    return pd.read_csv(path)


def section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def check_columns(df, columns, table_name):
    missing = [column for column in columns if column not in df.columns]

    if missing:
        print(f"{table_name}: Missing required columns: {missing}")
        return False

    return True


def main():
    customers = load_csv("customers.csv")
    orders = load_csv("orders.csv")
    items = load_csv("order_items.csv")
    products = load_csv("products.csv")
    returns = load_csv("returns.csv")

    tables = {
        "customers": customers,
        "orders": orders,
        "order_items": items,
        "products": products,
        "returns": returns,
    }

    # --------------------------------------------------
    # 1. BASIC DATA QUALITY
    # --------------------------------------------------

    section("1. BASIC DATA QUALITY")

    for name, df in tables.items():
        print(f"\n{name}.csv")
        print(f"Rows: {len(df):,}")
        print(f"Columns: {len(df.columns)}")
        print(f"Missing cells: {int(df.isna().sum().sum()):,}")
        print(f"Duplicate full rows: {int(df.duplicated().sum()):,}")

        id_columns = [
            column for column in df.columns
            if column.endswith("_id")
            and column in {
                "customer_id", "order_id", "order_item_id",
                "product_id", "return_id"
            }
        ]

        for column in id_columns:
            print(
                f"Duplicate {column}: "
                f"{int(df[column].duplicated().sum()):,}"
            )

    # --------------------------------------------------
    # 2. MISSING VALUES
    # --------------------------------------------------

    section("2. MISSING VALUES BY COLUMN")

    for name, df in tables.items():
        missing = df.isna().sum()
        missing = missing[missing > 0]

        print(f"\n{name}.csv")

        if missing.empty:
            print("No missing values.")
        else:
            print(missing.to_string())

    # --------------------------------------------------
    # 3. ORDER STATUS AND DELIVERY DAYS
    # --------------------------------------------------

    section("3. ORDER STATUS AND DELIVERY DAYS")

    if check_columns(
        orders, ["order_status", "delivery_days"], "orders"
    ):
        print("\nOrder status counts:")
        print(orders["order_status"].value_counts(dropna=False).to_string())

        print("\nMissing delivery_days by order status:")
        print(
            orders.groupby("order_status", dropna=False)["delivery_days"]
            .agg(total="size", missing="count")
            .assign(missing=lambda x: x["total"] - x["missing"])
            .to_string()
        )

        print("\nDelivery days summary:")
        print(orders["delivery_days"].describe().to_string())

        invalid_delivery = (
            orders["delivery_days"].notna()
            & (orders["delivery_days"] < 0)
        )
        print(
            "Orders with negative delivery_days:",
            int(invalid_delivery.sum())
        )

    # --------------------------------------------------
    # 4. CUSTOMER-ORDER RELATIONSHIPS
    # --------------------------------------------------

    section("4. CUSTOMER-ORDER RELATIONSHIPS")

    if check_columns(
        customers, ["customer_id"], "customers"
    ) and check_columns(
        orders, ["customer_id"], "orders"
    ):
        customer_ids = set(customers["customer_id"].dropna())
        order_customer_ids = set(orders["customer_id"].dropna())

        print("Unique customer IDs:", len(customer_ids))
        print("Unique customer IDs referenced by orders:", len(order_customer_ids))
        print(
            "Order customer IDs not found in customers:",
            len(order_customer_ids - customer_ids)
        )

    # --------------------------------------------------
    # 5. ORDER-ITEM RELATIONSHIPS
    # --------------------------------------------------

    section("5. ORDER-ITEM RELATIONSHIPS")

    if check_columns(orders, ["order_id"], "orders") and check_columns(
        items, ["order_id", "order_item_id"], "order_items"
    ):
        order_ids = set(orders["order_id"].dropna())
        item_order_ids = set(items["order_id"].dropna())

        print("Orders:", len(order_ids))
        print("Orders referenced by order items:", len(item_order_ids))
        print(
            "Item order IDs not found in orders:",
            len(item_order_ids - order_ids)
        )

    # --------------------------------------------------
    # 6. PRODUCT RELATIONSHIPS
    # --------------------------------------------------

    section("6. PRODUCT RELATIONSHIPS")

    if check_columns(products, ["product_id"], "products") and check_columns(
        items, ["product_id"], "order_items"
    ):
        product_ids = set(products["product_id"].dropna())
        item_product_ids = set(items["product_id"].dropna())

        print("Products:", len(product_ids))
        print("Products referenced by order items:", len(item_product_ids))
        print(
            "Item product IDs not found in products:",
            len(item_product_ids - product_ids)
        )

    # --------------------------------------------------
    # 7. RETURN RELATIONSHIPS
    # --------------------------------------------------

    section("7. RETURN RELATIONSHIPS")

    if check_columns(
        returns, ["order_item_id", "order_id"], "returns"
    ) and check_columns(
        items, ["order_item_id", "order_id"], "order_items"
    ):
        item_ids = set(items["order_item_id"].dropna())
        return_item_ids = set(returns["order_item_id"].dropna())

        print(
            "Return item IDs not found in order_items:",
            len(return_item_ids - item_ids)
        )

        item_order_lookup = items.set_index("order_item_id")["order_id"]
        matched_order_ids = returns["order_item_id"].map(item_order_lookup)

        mismatch = (
            matched_order_ids.notna()
            & returns["order_id"].notna()
            & (matched_order_ids != returns["order_id"])
        )

        print("Returns with mismatched order IDs:", int(mismatch.sum()))

    # --------------------------------------------------
    # 8. PROFIT VALIDATION
    # --------------------------------------------------

    section("8. PROFIT VALIDATION")

    profit_columns = [
        "line_profit_usd", "line_total_usd",
        "quantity", "unit_cost_usd"
    ]

    if check_columns(items, profit_columns, "order_items"):
        expected_profit = (
            items["line_total_usd"]
            - items["quantity"] * items["unit_cost_usd"]
        )

        difference = (items["line_profit_usd"] - expected_profit).abs()
        invalid_profit = difference > 0.02

        print("Order items:", len(items))
        print("Profit formula mismatches (tolerance $0.02):",
              int(invalid_profit.sum()))
        print("Average line profit USD:", round(items["line_profit_usd"].mean(), 2))
        print("Median line profit USD:", round(items["line_profit_usd"].median(), 2))
        print("Total recorded line profit USD:", round(items["line_profit_usd"].sum(), 2))
        print("Negative-profit items:", int((items["line_profit_usd"] < 0).sum()))
        print("Zero-profit items:", int((items["line_profit_usd"] == 0).sum()))

        negative = items.loc[items["line_profit_usd"] < 0, "line_profit_usd"]

        if not negative.empty:
            print("Average negative line profit USD:", round(negative.mean(), 2))
            print("Median negative line profit USD:", round(negative.median(), 2))
            print("Minimum line profit USD:", round(negative.min(), 2))

    # --------------------------------------------------
    # 9. REFUND AND RETURN REASON ANALYSIS
    # --------------------------------------------------

    section("9. REFUND AND RETURN REASON ANALYSIS")

    refund_column = next(
        (c for c in ["refund_amount_usd", "refund_usd", "refund_amount"]
         if c in returns.columns),
        None
    )

    reason_column = next(
        (c for c in ["return_reason", "reason"]
         if c in returns.columns),
        None
    )

    if refund_column:
        refunds = pd.to_numeric(returns[refund_column], errors="coerce")

        print("Total returns:", len(returns))
        print("Total refund USD:", round(refunds.sum(), 2))
        print("Average refund USD:", round(refunds.mean(), 2))
        print("Zero refunds:", int((refunds == 0).sum()))
        print("Negative refunds:", int((refunds < 0).sum()))
        print("Missing or nonnumeric refunds:", int(refunds.isna().sum()))
    else:
        print("Refund amount column not found. Check returns.csv column names.")

    if reason_column:
        print("\nReturn reasons:")
        print(returns[reason_column].value_counts(dropna=False).to_string())
    else:
        print("Return reason column not found. Check returns.csv column names.")

    # --------------------------------------------------
    # 10. RETURN QUANTITY VALIDATION
    # --------------------------------------------------

    section("10. RETURN QUANTITY VALIDATION")

    if check_columns(
        items, ["order_item_id", "quantity"], "order_items"
    ) and check_columns(
        returns, ["order_item_id"], "returns"
    ):
        return_qty_column = next(
            (c for c in ["returned_quantity", "return_quantity", "quantity"]
             if c in returns.columns),
            None
        )

        if return_qty_column:
            returned_qty = pd.to_numeric(
                returns[return_qty_column], errors="coerce"
            )

            returned_by_item = (
                returns.assign(_returned_qty=returned_qty)
                .groupby("order_item_id")["_returned_qty"]
                .sum(min_count=1)
            )

            ordered_qty = items.set_index("order_item_id")["quantity"]
            comparison = pd.concat(
                [ordered_qty.rename("ordered"),
                 returned_by_item.rename("returned")],
                axis=1
            )

            over_returned = (
                comparison["returned"].notna()
                & (comparison["returned"] > comparison["ordered"])
            )

            print("Order items returned in excess of ordered quantity:",
                  int(over_returned.sum()))
        else:
            print("Return quantity column not found; quantity check skipped.")

    # --------------------------------------------------
    # 11. RETURN DATE VALIDATION
    # --------------------------------------------------

    section("11. RETURN DATE VALIDATION")

    return_date_column = next(
        (c for c in ["return_date", "returned_at", "created_at"]
         if c in returns.columns),
        None
    )

    order_date_column = next(
        (c for c in ["order_date", "purchase_date", "created_at"]
         if c in orders.columns),
        None
    )

    if return_date_column and order_date_column and check_columns(
        returns, ["order_id", return_date_column], "returns"
    ) and check_columns(orders, ["order_id", order_date_column], "orders"):
        return_dates = pd.to_datetime(
            returns[return_date_column], errors="coerce"
        )

        order_date_lookup = orders.set_index("order_id")[order_date_column]
        order_dates = pd.to_datetime(
            returns["order_id"].map(order_date_lookup), errors="coerce"
        )

        invalid_dates = (
            return_dates.isna()
            | order_dates.isna()
            | (return_dates < order_dates)
        )

        print("Invalid return dates or returns before order date:",
              int(invalid_dates.sum()))
    else:
        print("Suitable return/order date columns not found; date check skipped.")

    # --------------------------------------------------
    # 12. CUSTOMER FIRST-ORDER DATE VALIDATION
    # --------------------------------------------------

    section("12. CUSTOMER FIRST-ORDER DATE VALIDATION")

    customer_columns = [
        "first_order_date", "lifetime_orders", "lifetime_spend_usd"
    ]

    if check_columns(customers, customer_columns, "customers"):
        
        first_order_date = pd.to_datetime(
    customers["first_order_date"],
    format="%d-%m-%Y",
    errors="coerce"

        )

        no_first_order = first_order_date.isna()

        print("Customers missing first_order_date:",
              int(no_first_order.sum()))

        print(
            "Missing first_order_date but lifetime_orders > 0:",
            int((no_first_order & (customers["lifetime_orders"] > 0)).sum())
        )

        print(
            "Missing first_order_date but lifetime_spend_usd > 0:",
            int((no_first_order & (customers["lifetime_spend_usd"] > 0)).sum())
        )

    # --------------------------------------------------
    # FINISH
    # --------------------------------------------------

    section("AUDIT COMPLETE")
    print("No source CSV files were modified by this script.")
    print("Audit script completed successfully.")


# --------------------------------------------------
# RUN AUDIT AND SAVE REPORT ONCE
# --------------------------------------------------

if __name__ == "__main__":
    output = io.StringIO()

    try:
        with redirect_stdout(output):
            main()
    except Exception:
        with redirect_stdout(output):
            section("AUDIT ERROR")
            traceback.print_exc()

    report_text = output.getvalue()

    REPORT_PATH.write_text(report_text, encoding="utf-8")

    print(report_text)
    print(f"\nAudit report saved to: {REPORT_PATH}")
