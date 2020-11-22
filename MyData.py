import pandas as pd
import matplotlib.pyplot as plt


class MyData:
    visa_path: str = "transactions/csv/visa.csv"
    checkings_path: str = "transactions/csv/checking.csv"
    savings_path: str = "transactions/csv/savings.csv"

    def read_my_csv(path: str) -> pd.DataFrame:
        """Read in the data from transaction csv files

        Args:
            path (str): Path to the transaction csv file

        Returns:
            DataFrame: A tabulated data set from the provided csv file
        """
        csv_data: pd.DataFrame = pd.read_csv(path)
        return csv_data

    def write_my_csv(path: str, finished_data) -> None:
        """Write given data to a csv file. The file is created in the given path

        Args:
            path (str): [description]
            finished_data ([type]): [description]
        """
        finished_data.to_csv(path)

    def organize_data(
        data: pd.DataFrame, remove_columns=["Transaction Date"]
    ) -> pd.DataFrame:
        """Fix name of columns and remove useless ones.
        Args:
            data (DataFrame): A tabulated data set
            remove_columns (list, optional): The columns you would like to remove after cleanup.. Defaults to ["Transaction Date"].

        Returns:
            DataFrame: An organized tabulated data set
        """
        data["Transaction Date"] = pd.to_datetime(data["Transaction Date"])
        data["Year_Month"] = data["Transaction Date"].dt.strftime("%Y-%m")
        data = data.drop(columns=remove_columns)
        return data

    def group_datasets(frames: list) -> pd.DataFrame:
        """Combine multiple datasets together.

        Args:
            frames (list): A list of datasets to combine

        Returns:
            pd.DataFrame: A tabulated dataset combined from the provided frames
        """
        combined_frames = pd.concat(frames)
        return combined_frames

    def visualize_bar_graph(data) -> None:
        """Visualize the data in a bar graph

        Args:
            data ([type]): A tabulated dataset
        """
        data.plot.bar()
        plt.show()

    def sum_columns(data: pd.DataFrame, sum_column: str) -> pd.DataFrame:
        """Sum columns for income, expenses, etc.

        Args:
            data (pd.DataFrame): [description]
            sum_column (str): The column name to sum

        Returns:
            pd.DataFrame: [description]
        """
        summed_total: pd.DataFrame = data[sum_column].sum(axis=0)
        return summed_total


# Read
visa_data = MyData.read_my_csv(MyData.visa_path)
checkings_data = MyData.read_my_csv(MyData.checkings_path)
savings_data = MyData.read_my_csv(MyData.savings_path)

# Organize
visa_data = MyData.organize_data(visa_data, ["Card", "Transaction Date"])
checkings_data = MyData.organize_data(checkings_data)
savings_data = MyData.organize_data(savings_data)

# Group
frames = [visa_data, checkings_data, savings_data]
combined_data = MyData.group_datasets(frames)

# Group by Y-M and sort
# data_group = combined_data.groupby("Year_Month").sum().sort_values(by="Year_Month")

# Sum
expenseSum = MyData.sum_columns(combined_data, ["Expense"])
incomeSum = MyData.sum_columns(combined_data, ["Income"])
print(expenseSum)
print(incomeSum)

total = incomeSum - expenseSum
print(f"Your current total balance is {total} CAD")
