import pandas as pd
import matplotlib.pyplot as plt
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re


class MyData:
    def __init__(self, visa_path: str, checkings_path: str, savings_path: str):
        self.visa_path = visa_path
        self.checkings_path = checkings_path
        self.savings_path = savings_path

    def read_my_csv(path: str) -> pd.DataFrame:
        """Read in the data from transaction csv files.

        Args:
            path (str): Path to the transaction csv file.

        Returns:
            DataFrame: A tabulated data set from the provided csv file.
        """
        csv_data = pd.read_csv(path)
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
        """Fix name of columns and remove useless ones. Transaction Date will be come Date.
        Args:
            data (DataFrame): A tabulated data set
            remove_columns (list, optional): The columns you would like to remove after cleanup.. Defaults to ["Transaction Date"].

        Returns:
            DataFrame: An organized tabulated data set
        """
        data["Transaction Date"] = pd.to_datetime(data["Transaction Date"])
        data["Date"] = data["Transaction Date"].dt.strftime("%Y-%m")
        data = data.drop(columns=remove_columns)
        return data

    def combine_datasets(frames: list) -> pd.DataFrame:
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
        data = data[~(data["Date"] < lower_bound)]
        data = data[~(data["Date"] > upper_bound)]
        return data

    def remove_punctuation(text: str) -> str:
        no_punct = "".join([c for c in text if c not in string.punctuation])
        return no_punct

    def remove_stopwords(text: str) -> list:
        words = [w for w in text if w not in stopwords.words("english")]
        return words

    def word_lemmatizer(text: str) -> list:
        lemmatizer = WordNetLemmatizer()
        lemmed_text = [lemmatizer.lemmatize(i) for i in text]
        return lemmed_text

    def word_stemmer(text: str) -> list:
        stemmer = PorterStemmer()
        stemmerd = " ".join([stemmer.stem(i) for i in text])
        return stemmerd

    def remove_single_characters(text: str) -> str:
        text = re.sub(r"\s+[a-zA-Z]\s+", " ", text)
        return text
