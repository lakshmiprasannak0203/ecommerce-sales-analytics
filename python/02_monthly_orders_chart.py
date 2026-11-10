
import pandas as pd
import matplotlib.pyplot as plt

# Load the monthly order results
monthly_orders = pd.read_csv("data/cleaned/monthly_orders.csv")

# Convert the month column into dates
monthly_orders["order_month"] = pd.to_datetime(
    monthly_orders["order_month"]
)

# Create the line chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_orders["order_month"],
    monthly_orders["total_orders"],
    marker="o"
)

# Add chart title and labels
plt.title("Monthly Order Trend - Olist E-Commerce")
plt.xlabel("Month")
plt.ylabel("Number of Orders")

# Improve chart readability
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

# Save the chart
plt.savefig(
    "screenshots/monthly_orders_trend.png",
    dpi=300,
    bbox_inches="tight"
)

# Display the chart
plt.show()

print("Chart saved to screenshots/monthly_orders_trend.png")