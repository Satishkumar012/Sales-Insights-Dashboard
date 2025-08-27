import pandas as pd
import random
from faker import Faker
from sqlalchemy import create_engine, text
import urllib.parse

fake = Faker()
password = urllib.parse.quote_plus("Papa@123")
engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306")
with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS SalesInsightsDashboard"))
    conn.execute(text("USE SalesInsightsDashboard"))

engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306/SalesInsightsDashboard")

with engine.connect() as conn:    
    conn.execute(text("DROP TABLE IF EXISTS Orders"))
    conn.execute(text("DROP TABLE IF EXISTS Products"))
    conn.execute(text("DROP TABLE IF EXISTS Customers"))

    conn.execute(text("""
        CREATE TABLE Customers (
            customer_id INT PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            city VARCHAR(100)
        )
    """))

    conn.execute(text("""
        CREATE TABLE Products (
            product_id INT PRIMARY KEY,
            name VARCHAR(100),
            category VARCHAR(100),
            price DECIMAL(10,2)
        )
    """))

    conn.execute(text("""
        CREATE TABLE Orders (
            order_id INT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES Products(product_id)
        )
    """))

print("✅ Tables created successfully!")

customers = [(i, fake.name(), random.randint(18, 60), fake.city()) for i in range(1, 6)]
products = [(i, fake.word(), random.choice(["Electronics", "Clothing", "Food"]), round(random.uniform(10, 500), 2)) for i in range(1, 6)]
orders = [(i, random.randint(1, 5), random.randint(1, 5), random.randint(1, 3), fake.date_this_year()) for i in range(1, 11)]

customers_df = pd.DataFrame(customers, columns=["customer_id", "name", "age", "city"])
products_df = pd.DataFrame(products, columns=["product_id", "name", "category", "price"])
orders_df = pd.DataFrame(orders, columns=["order_id", "customer_id", "product_id", "quantity", "order_date"])

customers_df.to_sql("Customers", engine, if_exists="append", index=False)
products_df.to_sql("Products", engine, if_exists="append", index=False)
orders_df.to_sql("Orders", engine, if_exists="append", index=False)

print("✅ Data inserted successfully!")
