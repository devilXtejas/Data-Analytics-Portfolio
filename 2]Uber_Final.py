# Setup & Load Data¶
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore') 

df = pd.read_csv("Uber_Dataset.csv")

# 1️⃣	Data Cleaning & Preprocessing
#     o	Handle missing or inconsistent data.
#     o	Convert date/time columns to appropriate formats.
#     o	Standardize categorical variables.


# remove hidden spaces in column names
df.columns = df.columns.str.strip()  

#To check shape of data
print("Shape: ",df.shape)

print("\nType of data:\n ",df.dtypes)

#Description
print("\nDiscription:\n ",df.describe(include = "all"))

#Unique_values
print("\nUnique values: ",df.nunique())

#all null values
print("\nNull Values: ",df.isnull().sum())

#All columns name
print(df.columns)

# 🔧 FIX: keep Time as datetime first (for Hour extraction later)
df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
df['Time'] = pd.to_datetime(df['Time'], errors = 'coerce')  

#TO check duplicates
print(df.duplicated().sum())

# Handle missing values
df = df.dropna(subset=['Booking Status'])

#Fill numeric column with median
num_col = ['Avg VTAT','Avg CTAT','Cancelled Rides by Customer',
           'Cancelled Rides by Driver','Incomplete Rides',
           'Booking Value','Ride Distance','Driver Ratings','Customer Rating']
for col in num_col:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(df[col].median(), inplace=True)

#Fill categorical columns with 'unknown'
cat_col = ['Booking Status','Vehicle Type','Pickup Location','Drop Location',
           'Reason for cancelling by Customer','Driver Cancellation Reason',
           'Incomplete Rides Reason','Payment Method']
for col in cat_col:
    df[col] = df[col].astype(str).str.strip().str.title()
    df[col].fillna('Unknown', inplace = True)

print(df.isnull().sum()) #Should be zero or near-zero 

#Standardize categories
cols_to_standardize = ['Vehicle Type', 'Booking Status', 'Payment Method', 'Pickup Location', 'Drop Location']
df[cols_to_standardize] = df[cols_to_standardize].apply(lambda x: x.str.strip().str.title())

# 2️⃣	Descriptive Analysis

#     o	What are the most and least popular vehicle types?
vehicle_counts = df['Vehicle Type'].value_counts()
print(vehicle_counts)
vehicle_counts.plot(kind='bar', figsize=(8,4), title="Vehicle Type Popularity", color='r')
plt.show()
#     o	What is the average ride distance and booking value?
print("Avg distance: ",round(df['Ride Distance'].mean(),2))
print("Avg booking value: ",round(df['Booking Value'].mean(),2))


#     o	Distribution of ratings (drivers and customers).
sns.histplot(df['Driver Ratings'], bins=10, kde=True, color='r')
plt.title("Driver Rating Distribution")
plt.show()

sns.histplot(df['Customer Rating'], bins=10, kde=True, color='r')
plt.title("Customer Rating Distribution")
plt.show()


#     o	Most common cancellation reasons by customers and drivers.
print(df['Reason for cancelling by Customer'].value_counts().head(10))
print('\n')
print(df['Driver Cancellation Reason'].value_counts().head(10))

# 3.	Customer Behavior Insights
# 🔧 FIX: create DayOfWeek and Hour BEFORE filtering cancellations
df['DayOfWeek'] = df['Date'].dt.day_name()   # 🔧 FIX
df['Hour'] = df['Time'].dt.hour              # 🔧 FIX
df['Time'] = df['Time'].dt.time              # 🔧 FIX (keep pure time for reference)

#     o	Who are the frequent cancellers (by customer ID)?
df_cancel = df[df['Booking Status'].str.contains("Cancel", case=False)]
print(df_cancel['Customer ID'].value_counts().head(10))

#     o	Is there a pattern in cancellations by time of day or day of week?
sns.countplot(x='DayOfWeek', data=df_cancel,
              order=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])
plt.title("Cancellations by Day of Week")
plt.show()

sns.countplot(x='Hour', data=df_cancel)
plt.title("Cancellations by Hour")
plt.show()

#     o	Correlation between ride value, distance, and customer satisfaction.
cols = ['Booking Value','Ride Distance','Driver Ratings','Customer Rating']
sns.heatmap(df[cols].corr(), annot=True, cmap="coolwarm")
plt.show()

# 4.	Driver Performance Evaluation
#     o	Which drivers have the highest/lowest ratings?
print("Highest Driver Rating:", df['Driver Ratings'].max())
print("Lowest Driver Rating:", df['Driver Ratings'].min())
print("Average Driver Rating:", round(df['Driver Ratings'].mean(),2))

#     o	How many rides are being cancelled by drivers and why?
driver_cancels = df[df['Booking Status'].str.contains("cancel", case=False)]
print(driver_cancels['Driver Cancellation Reason'].value_counts())
print("Total driver cancellations:", driver_cancels.shape[0])

# 5.	Operational Metrics
#     o	Average VTAT and CTAT across vehicle types and locations.
print(df.groupby('Vehicle Type')[['Avg VTAT','Avg CTAT']].mean())

#     o	Identify peak demand locations and time slots.
# **Pickup locations**
pickup_counts = df['Pickup Location'].value_counts().head(10)
pickup_counts.plot(kind='bar', figsize=(10,4), color='purple', title="Top Pickup Locations")
plt.show()

# **Drop locations**
drop_counts = df['Drop Location'].value_counts().head(10)
drop_counts.plot(kind='bar', figsize=(10,4), color='orange', title="Top Drop Locations")
plt.show()

# **Time slots**
df['Hour'].value_counts().sort_index().plot(kind='bar', figsize=(10,4), color='green')
plt.title("Peak Demand by Hour")
plt.show()

