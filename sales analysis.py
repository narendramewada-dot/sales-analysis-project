import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('TkAgg')  # graph show hone ke liye

import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

# ========== 1️⃣ MySQL Connection ==========
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="narendra@2004",   # apna password yahan likh
    database="sales_analysis"   # apna DB name yahan likh
)

query = """
SELECT s.sale_id, s.product_id, p.product_name, p.category, p.price, 
       s.quantity, s.sale_date, s.region
FROM sales s
JOIN products p ON s.product_id = p.product_id;
"""
df = pd.read_sql(query, conn)
conn.close()

# ========== 2️⃣ Data Cleaning ==========
df['sale_date'] = pd.to_datetime(df['sale_date'])
df['month'] = df['sale_date'].dt.month_name()
df['total_sales'] = df['quantity'] * df['price']

# ========== 3️⃣ Analysis ==========
print("✅ Total Revenue:", df['total_sales'].sum())
print("\n✅ Top Selling Products:\n", df.groupby('product_name')['total_sales'].sum().sort_values(ascending=False))
print("\n✅ Monthly Sales:\n", df.groupby('month')['total_sales'].sum().sort_values())
print("\n✅ Region Sales:\n", df.groupby('region')['total_sales'].sum())

# ========== 4️⃣ Visualizations ==========

## 🟦 Top Selling Products
top_products = df.groupby('product_name')['total_sales'].sum().sort_values(ascending=False).head(5)
plt.figure(figsize=(8,5))
sns.barplot(x=top_products.values, y=top_products.index, palette='Blues_d')
plt.title("Top 5 Selling Products")
plt.xlabel("Total Sales")
plt.ylabel("Product")
plt.show()

## 🟩 Monthly Sales Trend
monthly_sales = df.groupby('month')['total_sales'].sum()
plt.figure(figsize=(8,5))
sns.lineplot(x=monthly_sales.index, y=monthly_sales.values, marker='o', color='green')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

## 🟧 Region-wise Sales
region_sales = df.groupby('region')['total_sales'].sum()
plt.figure(figsize=(6,6))
plt.pie(region_sales.values, labels=region_sales.index, autopct='%1.1f%%', startangle=90)
plt.title("Region-wise Sales Distribution")
plt.show()
