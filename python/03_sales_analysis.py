
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PROJECT: E-Commerce Sales & Customer Analytics
# TASK 3: Sales Revenue Analysis
# ==========================================

# 1. Load the datasets
order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
products = pd.read_csv("data/raw/olist_products_dataset.csv")
category_translation = pd.read_csv(
    "data/raw/product_category_name_translation.csv"
)

print("\n========== DATASET OVERVIEW ==========")
print(f"Order items: {len(order_items)}")
print(f"Orders: {len(orders)}")
print(f"Products: {len(products)}")

# 2. Calculate total product sales value
# Price is the product price, excluding freight.
total_sales = order_items["price"].sum()
total_freight = order_items["freight_value"].sum()

print("\n========== OVERALL SALES ==========")
print(f"Total product sales value: R$ {total_sales:,.2f}")
print(f"Total freight charges: R$ {total_freight:,.2f}")

# 3. Add order purchase dates to order items
sales_data = order_items.merge(
    orders[["order_id", "order_purchase_timestamp", "order_status"]],
    on="order_id",
    how="left"
)

# Convert purchase timestamp to datetime
sales_data["order_purchase_timestamp"] = pd.to_datetime(
    sales_data["order_purchase_timestamp"],
    errors="coerce"
)

# 4. Calculate monthly product sales value
sales_data["order_month"] = (
    sales_data["order_purchase_timestamp"].dt.to_period("M")
)

monthly_sales = (
    sales_data.groupby("order_month")["price"]
    .sum()
    .reset_index(name="total_sales")
)

print("\n========== MONTHLY PRODUCT SALES ==========")
print(monthly_sales.to_string(index=False))

# Save monthly sales results
monthly_sales["order_month"] = monthly_sales["order_month"].astype(str)
monthly_sales.to_csv(
    "data/cleaned/monthly_sales.csv",
    index=False
)

# 5. Find the month with the highest product sales
if not monthly_sales.empty:
    highest_sales_month = monthly_sales.loc[
        monthly_sales["total_sales"].idxmax()
    ]

    print("\n========== HIGHEST SALES MONTH ==========")
    print(f"Month: {highest_sales_month['order_month']}")
    print(f"Product sales: R$ {highest_sales_month['total_sales']:,.2f}")

# 6. Join products with English category names
products_with_category = products.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

# Add category names to order items
category_sales = order_items.merge(
    products_with_category[
        ["product_id", "product_category_name_english"]
    ],
    on="product_id",
    how="left"
)

# Calculate sales by product category
category_summary = (
    category_sales.groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .reset_index(name="total_sales")
)

category_summary["product_category_name_english"] = (
    category_summary["product_category_name_english"]
    .fillna("unknown")
)

print("\n========== TOP 10 CATEGORIES BY PRODUCT SALES ==========")
print(category_summary.head(10).to_string(index=False))

# Save category sales results
category_summary.to_csv(
    "data/cleaned/category_sales.csv",
    index=False
)

# 7. Create a monthly sales chart
chart_data = monthly_sales.copy()
chart_data["order_month"] = pd.to_datetime(
    chart_data["order_month"]
)

plt.figure(figsize=(12, 6))
plt.plot(
    chart_data["order_month"],
    chart_data["total_sales"],
    marker="o"
)

plt.title("Monthly Product Sales - Olist E-Commerce")
plt.xlabel("Month")
plt.ylabel("Product Sales Value (Brazilian R$)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "screenshots/monthly_sales_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nChart saved to screenshots/monthly_sales_trend.png")
print("Monthly results saved to data/cleaned/monthly_sales.csv")
print("Category results saved to data/cleaned/category_sales.csv")
print("\n========== SALES ANALYSIS COMPLETED ==========")