import pymysql as sql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

password = urllib.parse.quote_plus('Papa@123')

engine = create_engine(f'mysql+pymysql://root:{password}@127.0.0.1:3306/SalesInsightsDashboard')

customers = pd.DataFrame(columns=["customer_id", "name", "age", "city"])

products = pd.DataFrame(columns=["product_id", "name", "category", "price"])

orders = pd.DataFrame(columns=["order_id", "customer_id", "product_id", "quantity", "order_date"]) 

print('DataBase created successfully...')