
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PROJECT: E-Commerce Sales & Customer Analytics
# TASK 5: Delivery Performance Analysis
# ==========================================

# 1. Load the orders dataset
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

# 2. Convert delivery columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for column in date_columns:
    orders[column] = pd.to_datetime(
        orders[column],
        errors="coerce"
    )

# 3. Keep orders that were actually delivered
delivered_orders = orders[
    (orders["order_status"] == "delivered")
    & orders["order_delivered_customer_date"].notna()
    & orders["order_estimated_delivery_date"].notna()
].copy()

# 4. Calculate actual delivery time in days
delivered_orders["delivery_days"] = (
    delivered_orders["order_delivered_customer_date"]
    - delivered_orders["order_purchase_timestamp"]
).dt.total_seconds() / (24 * 60 * 60)

# 5. Calculate whether the order arrived late
delivered_orders["days_vs_estimate"] = (
    delivered_orders["order_delivered_customer_date"]
    - delivered_orders["order_estimated_delivery_date"]
).dt.total_seconds() / (24 * 60 * 60)

delivered_orders["delivery_status"] = (
    delivered_orders["days_vs_estimate"]
    .apply(lambda days: "Late" if days > 0 else "On time or early")
)

# 6. Calculate key delivery metrics
total_delivered = len(delivered_orders)
average_delivery_days = delivered_orders["delivery_days"].mean()
median_delivery_days = delivered_orders["delivery_days"].median()

late_orders = (
    delivered_orders["delivery_status"] == "Late"
).sum()

on_time_or_early_orders = (
    delivered_orders["delivery_status"] == "On time or early"
).sum()

late_percentage = late_orders / total_delivered * 100

print("\n========== DELIVERY PERFORMANCE ==========")
print(f"Delivered orders analyzed: {total_delivered:,}")
print(f"Average delivery time: {average_delivery_days:.2f} days")
print(f"Median delivery time: {median_delivery_days:.2f} days")
print(f"Late orders: {late_orders:,}")
print(f"On-time or early orders: {on_time_or_early_orders:,}")
print(f"Late delivery percentage: {late_percentage:.2f}%")

# 7. Show delivery status counts
print("\n========== DELIVERY STATUS COUNTS ==========")
print(delivered_orders["delivery_status"].value_counts())

# 8. Save detailed delivery results
delivered_orders.to_csv(
    "data/cleaned/delivery_analysis.csv",
    index=False
)

print("\nDetailed results saved to data/cleaned/delivery_analysis.csv")

# 9. Create a delivery status chart
status_counts = (
    delivered_orders["delivery_status"]
    .value_counts()
    .reindex(["On time or early", "Late"], fill_value=0)
)

plt.figure(figsize=(8, 5))
plt.bar(status_counts.index, status_counts.values)

plt.title("Delivery Performance: Late vs On Time or Early")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")
plt.tight_layout()

plt.savefig(
    "screenshots/delivery_performance.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("Chart saved to screenshots/delivery_performance.png")
print("\n========== DELIVERY ANALYSIS COMPLETED ==========")