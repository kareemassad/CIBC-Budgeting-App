import re
import dateutil
import os
from datetime import datetime
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier
from colorama import init, Fore, Style
from tabulate import tabulate


class Classify:
    def __init__(self, data="transactions/csv/new/AllData.csv"):
        """Load in the previous data (by default from `data`) and initialise the classifier

        Args:
            data (str, optional): The path to the data that is loaded in. Defaults to "transactions/csv/new/AllData.csv".
        """

        # allows dynamic training data to be used (i.e many accounts in a loop)
        self.trainingDataFile = data

        if os.path.exists(data):
            self.prev_data = pd.read_csv(self.trainingDataFile)
        else:
            self.prev_data = pd.DataFrame(columns=["date", "desc", "amount", "cat"])

        self.classifier = NaiveBayesClassifier(
            self._get_training(self.prev_data), self._extractor
        )

    def add_data(self, file_path: str, bank: str = "cibc"):
        """Add new data and interactively classify it.
        Args:
            file_path (string): The path of the csv file.
            bank (str, optional): Name of the bank the data belongs to. Defaults to "cibc".
        """

        if bank == "cibc":
            print("adding CIBC bank data!")
            self.new_data = self._read_cibc_csv(file_path)
        # elif bank == "TD":
        #     print("adding CIBC bank data!")
        #     self.new_data = self._read_cibc_csv(file_path)

        self._ask_with_guess(self.new_data)

        self.prev_data = pd.concat([self.prev_data, self.new_data])
        # save data to the same file we loaded earlier
        self.prev_data.to_csv(self.trainingDataFile, index=False)

    def _prepare_for_analysis(self):
        """Prepare data for analysis in pandas, setting index types and subsetting"""

        self.prev_data = self._make_date_index(self.prev_data)

        self.prev_data["cat"] = self.prev_data["cat"].str.strip()

        self.inc = self.prev_data[self.prev_data.amount > 0]
        self.out = self.prev_data[self.prev_data.amount < 0]
        self.out.amount = self.out.amount.abs()

        self.inc_noignore = self.inc[self.inc.cat != "Ignore"]
        self.inc_noexpignore = self.inc[
            (self.inc.cat != "Ignore") & (self.inc.cat != "Expenses")
        ]

        self.out_noignore = self.out[self.out.cat != "Ignore"]
        self.out_noexpignore = self.out[
            (self.out.cat != "Ignore") & (self.out.cat != "Expenses")
        ]

    def _read_categories(self) -> dict:
        """Read list of categories from categories.txt. These are the items the classifier could guess.

        Returns:
            dict: The categories the classifier could guess.
        """
        categories = {}

        with open("app/categories.txt") as f:
            for i, line in enumerate(f.readlines()):
                categories[i] = line.strip()

        return categories

    def _add_new_category(self, category: str):
        """Add a new category to categories.txt

        Args:
            category (str): The category being added.
        """
        with open("categories.txt", "a") as f:
            f.write("\n" + category)

    def _ask_with_guess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Interactively guess categories for each transaction in df, asking each time if the guess
        is correct

        Args:
            df (DataFrame): The dataframe containing your data.

        Returns:
            DataFrame: A dataframe with a new categories column that contains the classifier's guesses.
        """
        # Initialise colorama
        init()

        df["cat"] = ""

        categories = self._read_categories()

        for index, row in df.iterrows():

            # Generate the category numbers table from the list of categories
            cats_list = [[idnum, cat] for idnum, cat in categories.items()]
            cats_table = tabulate(cats_list)

            stripped_text = self._strip_numbers(row["desc"])

            # Guess a category using the classifier (only if there is data in the classifier)
            if len(self.classifier.train_set) > 1:
                guess = self.classifier.classify(stripped_text)
            else:
                guess = ""

            # Print list of categories
            print(chr(27) + "[2J")
            print(cats_table)
            print("\n\n")
            # Print transaction
            print("On: %s\t %.2f\n%s" % (row["date"], row["amount"], row["desc"]))
            print(Fore.RED + Style.BRIGHT + "My guess is: " + str(guess) + Fore.RESET)

            input_value = input("> ")

            if input_value.lower() == "q":
                # If the input was 'q' then quit
                return df
            if input_value == "":
                # If the input was blank then our guess was right!
                df.at[index, "cat"] = guess
                self.classifier.update([(stripped_text, guess)])
            else:
                # Otherwise, our guess was wrong
                try:
                    # Try converting the input to an integer category number
                    # If it works then we've entered a category
                    category_number = int(input_value)
                    category = categories[category_number]
                except ValueError:
                    # Otherwise, we've entered a new category, so add it to the list of
                    # categories
                    category = input_value
                    self._add_new_category(category)
                    categories = self._read_categories()

                # Write correct answer
                df.at[index, "cat"] = category
                # Update classifier
                self.classifier.update([(stripped_text, category)])

        return df

    def _make_date_index(self, df: pd.DataFrame) -> pd.DataFrame:
        """Make the index of df a Datetime index

        Args:
            df (DataFrame): Your csv data.

        Returns:
            DataFrame: Your data modified to use the date as the index
        """
        df.index = pd.DatetimeIndex(df.date.apply(dateutil.parser.parse, dayfirst=True))

        return df

    def _read_cibc_csv(self, file_path: str) -> pd.DataFrame:
        """Read a file in the CSV format that the CIBC Bank provides.

        Args:
            file_path (str): [description]

        Returns:
            DataFrame: A DataFrame with columns of 'date', 'desc', and 'amount'.
        """

        data = pd.read_csv(file_path)
        data["Transaction Date"] = pd.to_datetime(data["Transaction Date"])
        data["Year_Month"] = data["Transaction Date"].dt.strftime("%Y-%m")
        data["Year_Month"] = pd.to_datetime(data["Year_Month"])
        data["Year_Month"].min(), data["Year_Month"].max()
        data["Transaction"] = data["Income"].fillna(0) - data["Expense"].fillna(0)
        data.drop(columns=["Expense", "Income"])

        # Rename columns
        data.rename(
            columns={
                "Description": "desc",
                "Year_Month": "date",
                "Transaction": "amount",
            },
            inplace=True,
        )

        # cast types to columns for math
        df = data.astype({"desc": str, "date": str, "amount": float})
        return df

    def _get_training(self, df: pd.DataFrame) -> list:
        """Get training data for the classifier, consisting of tuples of (text, category)

        Args:
            df (DataFrame): Your csv data.

        Returns:
            list: The training data used for the classifier containing a tuple.
        """
        train = []
        subset = df[df["cat"] != ""]
        for i in subset.index:
            row = subset.iloc[i]
            new_desc = self._strip_numbers(row["desc"])
            train.append((new_desc, row["cat"]))

        return train

    def _extractor(self, doc: str) -> dict:
        """Extract tokens from a given string.

        Args:
            doc (str): The word to split.

        Returns:
            dict: The extracted tokens.
        """
        # TODO: Extend to extract words within words
        # For example, MUSICROOM should give MUSIC and ROOM
        tokens = self._split_by_multiple_delims(doc, [" ", "/"])

        features = {}

        for token in tokens:
            if token == "":
                continue
            features[token] = True

        return features

    def _strip_numbers(self, s: str) -> str:
        """Strip numbers from the given string.
        Args:
            s (str): The string to be stripped.

        Returns:
            str: A string with the numbers stripped.
        """
        return re.sub("[^A-Z ]", "", s)

    def _split_by_multiple_delims(self, s: str, delims: list) -> list:
        """Split the given string by the list of delimiters given.

        Args:
            s (str): The string to be changed.
            delims (list): Delimiters to apply on the string.

        Returns:
            list: A list of strings that were stripped from the given string.
        """
        regexp = "|".join(delims)

        return re.split(regexp, s)
