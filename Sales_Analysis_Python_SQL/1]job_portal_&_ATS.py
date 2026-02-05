import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

#1. Database Connection

def get_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "tejas",
        database = "job_portal_ats"
    )

#Test connection
if __name__ == "__main__":
    try:
        connection = get_connection()
        print("✅ Database connection successful")
        connection.close()
    except Exception as e:
        print("❌ Connection failed:", e)

#2. Load table into pandas
def load_table(table_name):
    conn = get_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    companies = load_table("companies")
    jobs = load_table("jobs")
    candidates = load_table("candidates")
    applications = load_table("applications")

#3. Load required tables

companies = load_table("companies")
jobs = load_table("jobs")
candidates = load_table("candidates")
applications = load_table("applications")

# 4. Visualization 1:
# Application Status Distribution

status_count = applications['current_status'].value_counts()

plt.figure()
status_count.plot(kind='bar')
plt.title("Application Status Distribution")
plt.xlabel("Status")
plt.ylabel("Number Of Applications")
plt.show()

# 5. Visualization 2:
# Jobs per Company

jobs_per_company = jobs.groupby("company_id").size()

plt.figure()
jobs_per_company.plot(kind="bar")
plt.title("Jobs Posted Per Company")
plt.xlabel("Company ID")
plt.ylabel("Nummber of Jobs")
plt.show()

#6. Visualization 3:
# Applications per Job

applications_per_job = applications.groupby("job_id").size()

plt.figure()
applications_per_job.plot(kind="bar")
plt.title("Applications per Job")
plt.xlabel("Job ID")
plt.ylabel("Number of Applications")
plt.show()