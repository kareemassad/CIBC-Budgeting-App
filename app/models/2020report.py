import pandas as pd
import matplotlib.pyplot as plt
import os

credit_data = pd.read_csv("transactions/csv/visa.csv")
checking_data = pd.read_csv("transactions/csv/checking.csv")
savings_data = pd.read_csv("transactions/csv/savings.csv")

# Update the Data Type for the Date Columns
# Create a New column that will show the Month and Year of the Transaction

credit_data["Transaction Date"] = pd.to_datetime(credit_data["Transaction Date"])
credit_data["Year_Month"] = credit_data["Transaction Date"].dt.strftime("%Y-%m")
checking_data["Transaction Date"] = pd.to_datetime(checking_data["Transaction Date"])
checking_data["Year_Month"] = checking_data["Transaction Date"].dt.strftime("%Y-%m")
savings_data["Transaction Date"] = pd.to_datetime(savings_data["Transaction Date"])
savings_data["Year_Month"] = savings_data["Transaction Date"].dt.strftime("%Y-%m")

# Set upper and lower bounds
credit_data = credit_data[~(credit_data["Transaction Date"] <= "2020-1-1")]
credit_data = credit_data[~(credit_data["Transaction Date"] >= "2021-1-1")]

checking_data = checking_data[~(checking_data["Transaction Date"] <= "2020-1-1")]
checking_data = checking_data[~(checking_data["Transaction Date"] >= "2021-1-1")]

savings_data = savings_data[~(savings_data["Transaction Date"] <= "2020-1-1")]
savings_data = savings_data[~(savings_data["Transaction Date"] >= "2021-1-1")]


# Remove unused columns
credit_data = credit_data.drop(columns=["Card", "Transaction Date"])
checking_data = checking_data.drop(columns=["Transaction Date"])
savings_data = savings_data.drop(columns=["Transaction Date"])

# Group
frames = [checking_data, savings_data, credit_data]
f_data = pd.concat(frames)

# visualize
data_group = f_data.groupby("Year_Month").sum().sort_values(by="Year_Month")

# Sum
expenseSum = data_group["Expense"].sum(axis=0)
incomeSum = data_group["Income"].sum(axis=0)
print(data_group)
print("Expense: ", expenseSum)
print("Income: ", incomeSum)

netTotal = incomeSum - expenseSum
print(f"In the 2020 year you have made {netTotal} CAD")

data_group.plot.bar()
plt.show()

# Write data to CSV
# write = data_group.to_csv(r"2019report.csv")
