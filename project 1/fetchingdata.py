import pymysql as sql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

password = urllib.parse.quote_plus('Papa@123')

engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306/SalesInsightsDashboard")

query = """
SELECT o.order_id, 
       c.name AS customer, 
       p.name AS product, 
       p.category, 
       p.price, 
       o.quantity, 
       o.order_date 
FROM Orders o 
JOIN Customers c ON o.customer_id = c.customer_id 
JOIN Products p ON o.product_id = p.product_id;
"""

df = pd.read_sql_query(query, engine)
print(df.head())

