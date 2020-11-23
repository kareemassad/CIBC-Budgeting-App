import pandas as pd
import matplotlib.pyplot as plt


class MyData:
    visa_path: str = "transactions/csv/visa.csv"
    checkings_path: str = "transactions/csv/checking.csv"
    savings_path: str = "transactions/csv/savings.csv"

    def read_my_csv(path: str) -> pd.DataFrame:
        """Read in the data from transaction csv files.

        Args:
            path (str): Path to the transaction csv file.

        Returns:
            DataFrame: A tabulated data set from the provided csv file.
        """
        csv_data: pd.DataFrame = pd.read_csv(path)
        return csv_data

    def write_my_csv(path: str, finished_data) -> None:
        """Write given data to a csv file. The file is created in the given path.

        Args:
            path (str): The path to the directory to create the csv file.
            finished_data ([type]): The final modifications of the data.
        """
        finished_data.to_csv(path)

    def organize_data(
        data: pd.DataFrame, remove_columns=["Transaction Date"]
    ) -> pd.DataFrame:
        """Fix name of columns and remove useless ones. Transaction Date will be come Year_Month.
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
            DataFrame: A tabulated dataset combined from the provided frames
        """
        combined_frames = pd.concat(frames)
        return combined_frames

    def visualize_bar_graph(data: pd.DataFrame) -> None:
        """Visualize the data in a bar graph

        Args:
            data (DataFrame): A tabulated dataset
        """
        data.plot.bar()
        plt.show()

    def sum_columns(data: pd.DataFrame, sum_column: str) -> pd.DataFrame:
        """Sum columns for income, expenses, etc.

        Args:
            data (DataFrame): Pre-organized tabulated data
            sum_column (str): The column name to sum

        Returns:
            DataFrame: A tabulated dataset
        """
        summed_total: pd.DataFrame = data[sum_column].sum(axis=0)
        return summed_total

    def set_data_bounds(
        data: pd.DataFrame, upper_bound: str, lower_bound: str
    ) -> pd.DataFrame:
        """Concatenate the data around 2 dates provided.

        Args:
            data (DataFrame): Pre-organized tabulated data
            upper_bound (str): The day you want the data to end in YY-MM-DD.
            lower_bound (str): The day you want the data to start in YY-MM-DD.

        Returns:
            DataFrame: A tabulated dataset
        """
        data = data[~(data["Year_Month"] < lower_bound)]
        data = data[~(data["Year_Month"] > upper_bound)]
        return data


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
combined_data = MyData.group_datasets(frames)

# Group by Y-M and sort
data_group = combined_data.groupby("Year_Month").sum().sort_values(by="Year_Month")

# Sum
expenseSum = MyData.sum_columns(combined_data, ["Expense"])
incomeSum = MyData.sum_columns(combined_data, ["Income"])

total = incomeSum[0] - expenseSum[0]
print(f"Your current total balance is {total} CAD")

# visualize
MyData.visualize_bar_graph(data_group)