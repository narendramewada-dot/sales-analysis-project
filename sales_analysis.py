import warnings
warnings.filterwarnings('ignore')
import matplotlib
matplotlib.use('TkAgg')

import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "narendra@2004",
    database = "sales_analysis")
query = """
SELECT s.sale_id, s.product_id, p.product_name, p.category, p.price, 
       s.quantity, s.sale_date, s.region
FROM sales s
JOIN products p ON s.product_id = p.product_id;
"""
df = pd.read_sql(query, conn)
conn.close()
print(df.head())

# data cleaning and prepration
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['month'] = df['sale_date'].dt.month_name()
df['total_sales'] = df['quantity'] * df['price']

#total Revenue
total_revenue = df['total_sales'].sum()
print("Total Revenue:",total_revenue)

# Top selling product
top_products = df.groupby('product_name')['total_sales'].sum().sort_values(ascending=False)
print(top_products)

# Monthly Sales Trend
monthly_sales = df.groupby('month')['total_sales'].sum().sort_values()
print(monthly_sales)

# Region Wise Sales
region_sales = df.groupby('region')['total_sales'].sum()
print(region_sales)

# Top Products
plt.figure(figsize=(8,5))
sns.barplot(x=top_products.values,
y=top_products.index,palette='Blues_d')
plt.title("Top Selling Products")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.show()

# Monthly Sales Trend 
plt.figure(figsize=(8,5))
sns.lineplot(x=monthly_sales.index,
y=monthly_sales.values,marker='o',
color='green')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylable("Revenue")
plt.show()

# Region Wise Sales
plt.figure(figsize=(6,6))
plt.pie(region_sales.values,
lables=region_sales.index,autopct='%1,1f%',
startangle=90)
plt.title("Region Wise Sales Distribution")
plt.show()

conn.close()


