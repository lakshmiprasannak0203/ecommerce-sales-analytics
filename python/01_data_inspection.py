
import pandas as pd

# ==========================================
# PROJECT: E-Commerce Sales & Customer Analytics
# TASK 1: Data Inspection and Monthly Orders
# ==========================================

# 1. Load the orders dataset
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")

# 2. Inspect the dataset
print("\n========== DATASET OVERVIEW ==========")
print(f"Total rows: {orders.shape[0]}")
print(f"Total columns: {orders.shape[1]}")
print(f"Unique order IDs: {orders['order_id'].nunique()}")

# 3. Check missing values
print("\n========== MISSING VALUES ==========")
print(orders.isnull().sum())

# 4. Check duplicate order IDs
print("\n========== DUPLICATE ORDER IDs ==========")
print(orders["order_id"].duplicated().sum())

# 5. Check order statuses
print("\n========== ORDER STATUSES ==========")
print(orders["order_status"].value_counts())

# 6. Convert purchase timestamps to datetime
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# 7. Extract the month of each order
orders["order_month"] = (
    orders["order_purchase_timestamp"].dt.to_period("M")
)

# 8. Count orders placed each month
monthly_orders = (
    orders.groupby("order_month")["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

print("\n========== MONTHLY ORDERS ==========")
print(monthly_orders.to_string(index=False))

# 9. Find the month with the most orders
if not monthly_orders.empty:
    highest_month = monthly_orders.loc[
        monthly_orders["total_orders"].idxmax()
    ]

    print("\n========== HIGHEST ORDER MONTH ==========")
    print(f"Month: {highest_month['order_month']}")
    print(f"Total orders: {highest_month['total_orders']}")

# 10. Save monthly results
monthly_orders["order_month"] = (
    monthly_orders["order_month"].astype(str)
)

monthly_orders.to_csv(
    "data/cleaned/monthly_orders.csv",
    index=False
)

print("\nMonthly results saved to data/cleaned/monthly_orders.csv")
print("\n========== ANALYSIS COMPLETED ==========")