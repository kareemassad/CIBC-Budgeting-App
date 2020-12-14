"""This file generates a report for the 2020 year based on bank transactions and the MyData class
"""

from MyData import *

# Path to data
MyData.visa_path = "transactions/csv/old/visa.csv"
MyData.checkings_path = "transactions/csv/old/checking.csv"
MyData.savings_path = "transactions/csv/old/savings.csv"

# Read
visa_data = MyData.read_my_csv(MyData.visa_path)
checkings_data = MyData.read_my_csv(MyData.checkings_path)
savings_data = MyData.read_my_csv(MyData.savings_path)

# Organize
visa_data = MyData.organize_data(visa_data, ["Card", "Transaction Date"])
checkings_data = MyData.organize_data(checkings_data)
savings_data = MyData.organize_data(savings_data)


# Set bounds to  2020/2021
lower_bound = "2020-01"
upper_bound = "2021-01"

visa_data = MyData.set_data_bounds(visa_data, upper_bound, lower_bound)
checkings_data = MyData.set_data_bounds(checkings_data, upper_bound, lower_bound)
savings_data = MyData.set_data_bounds(savings_data, upper_bound, lower_bound)

# Group
frames = [visa_data, checkings_data, savings_data]
combined_data = MyData.combine_datasets(frames)

combined_data["Year_Month"] = pd.to_datetime(combined_data["Year_Month"])
combined_data["Year_Month"].min(), combined_data["Year_Month"].max()


combined_data["Transaction"] = combined_data["Income"].fillna(0) - combined_data[
    "Expense"
].fillna(0)

combined_data.drop(columns=["Expense", "Income"])
print(combined_data)

# # Group by Y-M and sort
# data_group = combined_data.groupby("Year_Month").sum()
# print(data_group)
# # Sum
# expenseSum = MyData.sum_columns(data_group, ["Expense"])
# incomeSum = MyData.sum_columns(data_group, ["Income"])

# total = incomeSum[0] - expenseSum[0]
# print(f"Your current total balance is {total} CAD")

# # visualize
# MyData.visualize_bar_graph(data_group)

# # Write csv
# MyData.write_my_csv("transactions/csv/new/all_data.csv", combined_data)
# MyData.write_my_csv("transactions/csv/new/income_expenses.csv", data_group)