import re
import dateutil
import os
from datetime import datetime
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier
from colorama import init, Fore, Style
from tabulate import tabulate


class BankClassify:
    def __init__(self, data="AllData.csv"):
        """Load in the previous data (by default from `data`) and initialise the classifier"""

        # allows dynamic training data to be used (i.e many accounts in a loop)
        self.trainingDataFile = data

        if os.path.exists(data):
            self.prev_data = pd.read_csv(self.trainingDataFile)
        else:
            self.prev_data = pd.DataFrame(columns=["date", "desc", "amount", "cat"])

        self.classifier = NaiveBayesClassifier(
            self._get_training(self.prev_data), self._extractor
        )

    def add_data(self, filename, bank="cibc"):
        """Add new data and interactively classify it.
        Arguments:
         - filename: filename and path of file
        """
        if bank == "cibc":
            print("adding CIBC bank data!")
            self.new_data = self._read_cibc_csv(filename)
        # elif bank == "TD":
        #     print("adding CIBC bank data!")
        #     self.new_data = self._read_cibc_csv(filename)

        self._ask_with_guess(self.new_data)

        self.prev_data = pd.concat([self.prev_data, self.new_data])
        # save data to the same file we loaded earlier
        self.prev_data.to_csv(self.trainingDataFile, index=False)

    def _prep_for_analysis(self):
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

    def _read_categories(self):
        """Read list of categories from categories.txt"""
        categories = {}

        with open("app/categories.txt") as f:
            for i, line in enumerate(f.readlines()):
                categories[i] = line.strip()

        return categories

    def _add_new_category(self, category):
        """Add a new category to categories.txt"""
        with open("categories.txt", "a") as f:
            f.write("\n" + category)

    def _ask_with_guess(self, df):
        """Interactively guess categories for each transaction in df, asking each time if the guess
        is correct"""
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

    def _make_date_index(self, df):
        """Make the index of df a Datetime index"""
        df.index = pd.DatetimeIndex(df.date.apply(dateutil.parser.parse, dayfirst=True))

        return df

    def _read_nationwide_file(self, filename):
        """Read a file in the csv file that Nationwide provides downloads in.
        Returns a pd.DataFrame with columns of 'date', 'desc' and 'amount'."""

        with open(filename) as f:
            lines = f.readlines()

        dates = []
        descs = []
        amounts = []

        for line in lines[5:]:

            line = "".join(i for i in line if ord(i) < 128)
            if line.strip() == "":
                continue

            splits = line.split('","')
            """
            0 = Date
            1 = Transaction type
            2 = Description
            3 = Paid Out
            4 = Paid In
            5 = Balance
            """
            date = splits[0].replace('"', "").strip()
            date = datetime.strptime(date, "%d %b %Y").strftime("%d/%m/%Y")
            dates.append(date)

            # get spend/pay in amount
            if splits[3] != "":  # paid out
                spend = float(re.sub("[^0-9\.-]", "", splits[3])) * -1
            else:  # paid in
                spend = float(re.sub("[^0-9\.-]", "", splits[4]))

            amounts.append(spend)

            # Description
            descs.append(splits[2])

        df = pd.DataFrame({"date": dates, "desc": descs, "amount": amounts})

        df["amount"] = df.amount.astype(float)
        df["desc"] = df.desc.astype(str)
        df["date"] = df.date.astype(str)

        return df

    def _read_cibc_csv(self, filename):
        """Read a file in the CSV format that CIBC Bank provides downloads in.
        Returns a pd.DataFrame with columns of 'date', 'desc', and 'amount'."""

        data = pd.read_csv(filename)
        data["Transaction Date"] = pd.to_datetime(data["Transaction Date"])
        data["Year_Month"] = data["Transaction Date"].dt.strftime("%Y-%m")
        data["Year_Month"] = pd.to_datetime(data["Year_Month"])
        data["Year_Month"].min(), data["Year_Month"].max()
        data["Transaction"] = data["Income"].fillna(0) - data["Expense"].fillna(0)
        data.drop(columns=["Expense", "Income"])

        """Rename columns """
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

    def _get_training(self, df):
        """Get training data for the classifier, consisting of tuples of
        (text, category)"""
        train = []
        subset = df[df["cat"] != ""]
        for i in subset.index:
            row = subset.iloc[i]
            new_desc = self._strip_numbers(row["desc"])
            train.append((new_desc, row["cat"]))

        return train

    def _extractor(self, doc):
        """Extract tokens from a given string"""
        # TODO: Extend to extract words within words
        # For example, MUSICROOM should give MUSIC and ROOM
        tokens = self._split_by_multiple_delims(doc, [" ", "/"])

        features = {}

        for token in tokens:
            if token == "":
                continue
            features[token] = True

        return features

    def _strip_numbers(self, s):
        """Strip numbers from the given string"""
        return re.sub("[^A-Z ]", "", s)

    def _split_by_multiple_delims(self, string, delims):
        """Split the given string by the list of delimiters given"""
        regexp = "|".join(delims)

        return re.split(regexp, string)