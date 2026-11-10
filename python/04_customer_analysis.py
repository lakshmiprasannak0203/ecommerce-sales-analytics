
import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
customers = pd.read_csv("data/raw/olist_customers_dataset.csv")

# Join orders with customer information
customer_orders = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

# Count orders placed by each unique customer
orders_per_customer = (
    customer_orders.groupby("customer_unique_id")["order_id"]
    .nunique()
    .reset_index(name="total_orders")
)

# Calculate customer metrics
total_customers = customer_orders["customer_unique_id"].nunique()

repeat_customers = (
    orders_per_customer["total_orders"] > 1
).sum()

one_time_customers = (
    orders_per_customer["total_orders"] == 1
).sum()

repeat_rate = repeat_customers / total_customers * 100

print("\n========== CUSTOMER ANALYSIS ==========")
print(f"Unique customers: {total_customers:,}")
print(f"One-time customers: {one_time_customers:,}")
print(f"Repeat customers: {repeat_customers:,}")
print(f"Repeat customer rate: {repeat_rate:.2f}%")

# Analyze customers by state
customers_by_state = (
    customer_orders.groupby("customer_state")["customer_unique_id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index(name="unique_customers")
)

print("\n========== TOP 10 STATES BY CUSTOMERS ==========")
print(customers_by_state.head(10).to_string(index=False))

# Save results
orders_per_customer.to_csv(
    "data/cleaned/orders_per_customer.csv",
    index=False
)

customers_by_state.to_csv(
    "data/cleaned/customers_by_state.csv",
    index=False
)

# Plot the top 10 states
top_states = customers_by_state.head(10).sort_values(
    "unique_customers"
)

plt.figure(figsize=(10, 6))
plt.barh(
    top_states["customer_state"],
    top_states["unique_customers"]
)

plt.title("Top 10 Brazilian States by Unique Customers")
plt.xlabel("Number of Unique Customers")
plt.ylabel("State")
plt.tight_layout()

plt.savefig(
    "screenshots/top_customer_states.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nCustomer analysis completed!")