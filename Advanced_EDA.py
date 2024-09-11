import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Load the data
df = pd.read_csv('SaaS-Sales.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 1. Time Series Decomposition
def time_series_decomposition(df):
    monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly_sales['Order Date'] = monthly_sales['Order Date'].dt.to_timestamp()
    monthly_sales.set_index('Order Date', inplace=True)
    
    decomposition = seasonal_decompose(monthly_sales['Sales'], model='additive', period=12)
    
    plt.figure(figsize=(16, 12))
    plt.subplot(411)
    plt.plot(decomposition.observed)
    plt.title('Observed')
    plt.subplot(412)
    plt.plot(decomposition.trend)
    plt.title('Trend')
    plt.subplot(413)
    plt.plot(decomposition.seasonal)
    plt.title('Seasonal')
    plt.subplot(414)
    plt.plot(decomposition.resid)
    plt.title('Residual')
    plt.tight_layout()
    plt.show()

# 2. Customer Segmentation using K-means Clustering
def customer_segmentation(df):
    customer_features = df.groupby('Customer ID').agg({
        'Sales': 'sum',
        'Quantity': 'sum',
        'Discount': 'mean',
        'Profit': 'sum',
        'Order ID': 'count'
    }).reset_index()
    customer_features.rename(columns={'Order ID': 'Frequency'}, inplace=True)
    
    features = ['Sales', 'Quantity', 'Discount', 'Profit', 'Frequency']
    X = customer_features[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=4, random_state=42)
    customer_features['Cluster'] = kmeans.fit_predict(X_scaled)
    
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=customer_features, x='Sales', y='Profit', hue='Cluster', size='Frequency', palette='viridis')
    plt.title('Customer Segments')
    plt.show()
    
    print(customer_features.groupby('Cluster')[features].mean())

# 3. Predictive Modeling for Sales Forecasting
def sales_forecasting(df):
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['Day'] = df['Order Date'].dt.day
    df['DayOfWeek'] = df['Order Date'].dt.dayofweek
    
    features = ['Year', 'Month', 'Day', 'DayOfWeek', 'Quantity', 'Discount']
    X = df[features]
    y = df['Sales']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared Score: {r2}")
    
    feature_importance = pd.DataFrame({
        'feature': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='importance', y='feature', data=feature_importance)
    plt.title('Feature Importance for Sales Prediction')
    plt.show()

# 4. Cohort Analysis
def cohort_analysis(df):
    df['CohortMonth'] = df['Order Date'].dt.to_period('M')
    df['CohortIndex'] = (df['Order Date'].dt.to_period('M') - 
                         df.groupby('Customer ID')['Order Date'].transform('min').dt.to_period('M')).apply(lambda x: x.n)
    
    cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['Customer ID'].nunique().reset_index()
    cohort_data = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='Customer ID')
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(cohort_data.T, cmap='YlOrRd', annot=True, fmt='g')
    plt.title('Customer Cohort Analysis')
    plt.xlabel('Cohort Month')
    plt.ylabel('Cohort Index')
    plt.show()

# 5. Market Basket Analysis
def market_basket_analysis(df):
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    
    basket = df.groupby(['Order ID', 'Product'])['Quantity'].sum().unstack().reset_index().fillna(0)
    basket = basket.set_index('Order ID')
    basket_sets = basket.applymap(lambda x: 1 if x > 0 else 0)
    
    frequent_itemsets = apriori(basket_sets, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    print(rules.sort_values('lift', ascending=False).head(10))

# Run advanced analyses
TSD = time_series_decomposition(df)
CS = customer_segmentation(df)
SF = sales_forecasting(df)
CA = cohort_analysis(df)
MB = market_basket_analysis(df)
