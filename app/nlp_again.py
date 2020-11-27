from MyData import *
from nltk.stem import WordNetLemmatizer
import numpy as np
import re
import nltk
from sklearn.datasets import load_files
import pickle
from nltk.corpus import stopwords

stemmer = WordNetLemmatizer()

df = pd.read_csv("app/test.csv")

df = MyData.organize_data(df)
df = df.drop(columns=["Expense", "Income", "Year_Month"])
data = df["Description"].values

for x in range(0, len(data)):
    data = re.sub(r"\W", " ", data[x])

print(data)