import pymysql as sql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

password = urllib.parse.quote_plus('Papa@123')
engine = create_engine(f'mysql+pymysql://root:{password}@127.0.0.1:3306/SalesInsightsDashboard')

customers = pd.read_sql("SELECT * FROM Customers", engine)
products = pd.read_sql("SELECT * FROM Products", engine)
orders = pd.read_sql("SELECT * FROM Orders", engine)

customers = customers.rename(columns={"name": "customer_name"})
products = products.rename(columns={"name": "product_name"})

df = orders.merge(customers, on="customer_id", how="left") \
           .merge(products, on="product_id", how="left")

df["revenue"] = df["price"] * df["quantity"]

total_revenue = df["revenue"].sum()

avg_order_value = df.groupby("order_id")["revenue"].sum().mean()

top_customers = (
    df.groupby("customer_name")["revenue"]
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M")
monthly_sales = df.groupby("month")["revenue"].sum()

print("✅ Total Revenue:", total_revenue)
print("✅ Average Order Value:", avg_order_value)
print("\n✅ Top 5 Customers:\n", top_customers)
print("\n✅ Monthly Sales:\n", monthly_sales)
