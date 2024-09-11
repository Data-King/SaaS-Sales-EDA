import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Load the data
df = pd.read_csv('SaaS-Sales.csv')  # Replace with your actual file path
#convert order date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])




# Sales Performance Analysis
def sales_performance_analysis(df):
    print("1. Sales Performance Analysis")
    
    # Total sales and profit over time
    monthly_data = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly_data['Order Date'] = monthly_data['Order Date'].dt.to_timestamp()
    
    plt.figure(figsize=(12, 6))
    plt.plot(monthly_data['Order Date'], monthly_data['Sales'], label='Sales')
    plt.plot(monthly_data['Order Date'], monthly_data['Profit'], label='Profit')
    plt.title('Total Sales and Profit Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()




# Top 10 performing products
    top_products = df.groupby('Product').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).sort_values('Sales', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    top_products.plot(kind='bar')
    plt.title('Top 10 Products by Sales and Profit')
    plt.xlabel('Product')
    plt.ylabel('Amount')
    plt.xticks(rotation=45, ha='right')
    plt.legend(['Sales', 'Profit'])
    plt.tight_layout()
    plt.show()
    
    # Discount effectiveness
    df['Discount_Bin'] = pd.cut(df['Discount'], bins=[0, 0.1, 0.2, 0.3, 0.4, 1], labels=['0-10%', '10-20%', '20-30%', '30-40%', '40%+'])
    discount_effect = df.groupby('Discount_Bin').agg({
        'Sales': 'mean',
        'Profit': 'mean'
    })
    
    plt.figure(figsize=(10, 6))
    discount_effect.plot(kind='bar')
    plt.title('Effect of Discount on Average Sales and Profit')
    plt.xlabel('Discount Range')
    plt.ylabel('Average Amount')
    plt.legend(['Sales', 'Profit'])
    plt.tight_layout()
    plt.show()



# Customer Segmentation Analysis
def customer_segmentation_analysis(df):
    print("\n2. Customer Segmentation Analysis")
    
    # Performance across customer segments
    segment_performance = df.groupby('Segment').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).rename(columns={'Order ID': 'Order Count'})
    
    print(segment_performance)
    
    # Industry-specific trends
    industry_trends = df.groupby('Industry').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).sort_values('Sales', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    industry_trends['Sales'].plot(kind='bar')
    plt.title('Top 10 Industries by Sales')
    plt.xlabel('Industry')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def geographical_analysis(df):
    print("\n3. Geographical Analysis")
    
    # Sales by country
    country_sales = df.groupby('Country')['Sales'].sum().sort_values(ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    country_sales.plot(kind='bar')
    plt.title('Top 10 Countries by Sales')
    plt.xlabel('Country')
    plt.ylabel('Total Sales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
    
    # Region performance
    region_performance = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Order ID': 'count'
    }).sort_values('Sales', ascending=False)
    
    print("Region Performance:")
    print(region_performance)

def product_analysis(df):
    print("\n4. Product Analysis")
    
    # Product popularity and profitability
    product_metrics = df.groupby('Product').agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum'
    }).sort_values('Sales', ascending=False).head(10)
    
    product_metrics['Profit Margin'] = product_metrics['Profit'] / product_metrics['Sales']
    
    print("Top 10 Products by Sales:")
    print(product_metrics)
    
    # Product performance across segments
    product_segment = df.groupby(['Product', 'Segment'])['Sales'].sum().unstack()
    product_segment_top = product_segment.sort_values('SMB', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    product_segment_top.plot(kind='bar', stacked=True)
    plt.title('Top 10 Products Performance Across Segments')
    plt.xlabel('Product')
    plt.ylabel('Total Sales')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Time-based Analysis
def time_based_analysis(df):
    print("\n5. Time-based Analysis")
    
    # Seasonal trends
    df['Month'] = df['Order Date'].dt.month
    monthly_sales = df.groupby('Month')['Sales'].mean()
    
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='line', marker='o')
    plt.title('Average Monthly Sales (Seasonal Trend)')
    plt.xlabel('Month')
    plt.ylabel('Average Sales')
    plt.xticks(range(1, 13))
    plt.tight_layout()
    plt.show()
    
    # Year-over-year growth
    df['Year'] = df['Order Date'].dt.year
    yearly_sales = df.groupby('Year')['Sales'].sum()
    yoy_growth = yearly_sales.pct_change() * 100
    
    print("Year-over-Year Sales Growth:")
    print(yoy_growth)



# Discount Analysis
def discount_analysis(df):
    print("\n6. Discount Analysis")
    
    df['Discount_Bin'] = pd.cut(df['Discount'], bins=[0, 0.1, 0.2, 0.3, 0.4, 1], labels=['0-10%', '10-20%', '20-30%', '30-40%', '40%+'])
    discount_impact = df.groupby('Discount_Bin').agg({
        'Sales': 'mean',
        'Profit': 'mean',
        'Quantity': 'mean'
    })
    
    print("Impact of Discounts on Sales, Profit, and Quantity:")
    print(discount_impact)
    
    # Optimal discount by product
    product_discount = df.groupby(['Product', 'Discount_Bin'])['Profit'].mean().unstack()
    optimal_discount = product_discount.idxmax(axis=1).value_counts()
    
    plt.figure(figsize=(10, 6))
    optimal_discount.plot(kind='bar')
    plt.title('Optimal Discount Ranges for Products')
    plt.xlabel('Discount Range')
    plt.ylabel('Number of Products')
    plt.tight_layout()
    plt.show()



# Customer Behavior Analysis
def customer_behavior_analysis(df):
    print("\n7. Customer Behavior Analysis")
    
    customer_metrics = df.groupby('Customer').agg({
        'Order ID': 'count',
        'Sales': ['mean', 'sum']
    })
    
    customer_metrics.columns = ['Purchase Frequency', 'Avg Order Value', 'Total Spend']
    
    customer_metrics = customer_metrics.sort_values('Total Spend', ascending=False)
    
    print("Top 10 Customers by Total Spend:")
    print(customer_metrics.head(10))
    
    plt.figure(figsize=(10, 6))
    plt.scatter(customer_metrics['Purchase Frequency'], customer_metrics['Avg Order Value'], alpha=0.5)
    plt.title('Customer Purchase Frequency vs Average Order Value')
    plt.xlabel('Purchase Frequency')
    plt.ylabel('Average Order Value')
    plt.tight_layout()
    plt.show()


# Profitability Analysis
def profitability_analysis(df):
    print("\n8. Profitability Analysis")
    
    df['Profit Margin'] = df['Profit'] / df['Sales']
    
    # Profitability by product
    product_profitability = df.groupby('Product').agg({
        'Profit Margin': 'mean',
        'Sales': 'sum',
        'Profit': 'sum'
    }).sort_values('Profit', ascending=False).head(10)
    
    print("Top 10 Most Profitable Products:")
    print(product_profitability)
    
    # Profitability by region
    region_profitability = df.groupby('Region').agg({
        'Profit Margin': 'mean',
        'Sales': 'sum',
        'Profit': 'sum'
    }).sort_values('Profit', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=region_profitability.reset_index(), x='Sales', y='Profit', size='Profit Margin', sizes=(50, 500), alpha=0.7)
    plt.title('Regional Profitability')
    plt.xlabel('Total Sales')
    plt.ylabel('Total Profit')
    for i, row in region_profitability.reset_index().iterrows():
        plt.annotate(row['Region'], (row['Sales'], row['Profit']))
    plt.tight_layout()
    plt.show()

# Run all analyses
SPA = sales_performance_analysis(df)
CSA = customer_segmentation_analysis(df)
GA  = geographical_analysis(df)
PA  =  product_analysis(df)
TBA = time_based_analysis(df)
DA  = discount_analysis(df)
CBA = customer_behavior_analysis(df)
PA  = profitability_analysis(df)


#run all the functions
SPA
CSA
GA
PA
TBA
DA
CBA
PA
