import pandas as pd

# 1. Load Dataset
df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("✅ Dataset loaded successfully")

# 2. Basic Information
print("\nShape of dataset (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

# 3. First 5 rows
print("\nFirst 5 rows:")
print(df.head())

# 4. Last 5 rows
print("\nLast 5 rows:")
print(df.tail())

# 5. Missing values check
print("\nMissing values per column:")
print(df.isnull().sum())


#DATA CLEANING:

# 1] Check unique values in Churn column
print("\n Unique value in churn column: ")
print(df['Churn'].unique())

# 2] Fix TotalCharges column
df["TotalCharges"] = pd.to_numeric(df['TotalCharges'], errors="coerce")

print("\nData type after fixing TotalCharges: ")
print(df['TotalCharges'].dtype)

# 3] Check missing value again
print("\nMIssing values after conversion: ")
print(df.isnull().sum())

# 4] Handling missing values
print("Rows before dropna:", df.shape[0])
df = df.dropna()
print("Rows after dropna:", df.shape[0])

print("\nShape after removing missing values:")
print(df.shape)

# 5] Verufy no missing values remain
print("\nFinal missing values check:") 
print(df.isnull().sum())


# Exploratory Data Analysis(EDA)

# 1] Overall churn distributiion
print("\nOverall Churn Distribution: ")
churn_count = df['Churn'].value_counts()
print(churn_count)

print("\nChurn Percentage: ")
churn_percent = df["Churn"].value_counts(normalize=True) * 100
for i, value in churn_percent.items():
    print(f"{i} : {value:.2f}%")
# print(f"{churn_percent.round(2)}")

# 2] Churn by gender
print("\nChurn by gender: ")
churn_by_gender = df.groupby("gender")['Churn'].value_counts(normalize=True)*100
for i, value in churn_by_gender.items():
    print(f"{i} : {value:.2f}%")
#print(f"{churn_by_gender.round(2)}")    

# 3] Churn by senior citizen
print("\Churn by senior citizen: ")
churn_by_senior = df.groupby('SeniorCitizen')['Churn'].value_counts(normalize=True)*100
print(churn_by_senior.round(2))
# for i, value in churn_by_senior.items():
#     print(f"{i} : {value:.2f}%")

# 4] Average tenure by churn
print("\nAverage Tenure by Churn:")
avg_tenure = df.groupby("Churn")["tenure"].mean()
print(avg_tenure.round(2))

# 5] Average monthly charges by churn
print("\nAverage Monthly Charges by Churn:")
avg_monthly = df.groupby("Churn")["MonthlyCharges"].mean()
print(avg_monthly.round(2))


# Data Visualization

import seaborn as sns
import matplotlib.pyplot as plt

sns.set(style='darkgrid')#Toset seaborn style

# 1]churn distribution
plt.figure()
sns.countplot(x='Churn', data=df)
plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")
plt.show()

# 2] Churn by gender

plt.figure()
sns.countplot(x="gender", hue="Churn", data=df)
plt.title("Churn by Gender")
plt.xlabel("Gender")
plt.ylabel("Count")
plt.show()

# 3] Churn by Senior Citizen
plt.figure()
sns.countplot(x="SeniorCitizen", hue="Churn", data=df)
plt.title("Churn by Senior Citizen")
plt.xlabel("Senior Citizen (0 = No, 1 = Yes)")
plt.ylabel("Count")
plt.show()

# 4] Tenure vs Churn
plt.figure()
sns.boxplot(x="Churn", y="tenure", data=df)
plt.title("Tenure vs Churn")
plt.xlabel("Churn")
plt.ylabel("Tenure (months)")
plt.show()

# 5] Monthly Charges vs Churn
plt.figure()
sns.boxplot(x="Churn", y="MonthlyCharges", data=df)
plt.title("Monthly Charges vs Churn")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")
plt.show()