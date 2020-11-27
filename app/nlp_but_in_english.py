from nltk.tokenize import RegexpTokenizer
from MyData import *


df = pd.read_csv("app/test.csv")

df = MyData.organize_data(df)
df = df.drop(columns=["Expense", "Income"])

# Regex
# \w means ASCII, numbers, and underscores. + means linked chars
# More ex:  (\w+|\$[\d\.]+|\S+) = splits up by spaces or by periods that are not attached to a digit
#           (\s+, gaps=True) = grabs everything except spaces as a token
#           ([A-Z]\w+) = only words that begin with a capital letter.
tokenizer = RegexpTokenizer(r"\w+")
# Remove Punctuation
df["Description"] = df["Description"].apply(lambda x: MyData.remove_punctuation(x))
# tokenize into single words
df["Description"] = df["Description"].apply(lambda x: tokenizer.tokenize(x.lower()))
# remove stop words such as The, Of, And etc..
df["Description"] = df["Description"].apply(lambda x: MyData.remove_stopwords(x))
# Lemmatize! (Maps common words into base ones from the dictionary)
df["Description"] = df["Description"].apply(lambda x: MyData.word_lemmatizer(x))

# MyData.write_my_csv("transactions/csv/new/nlp.csv", df)
# Use PorterStemmer (Aggressing lemmatizing essentially), Cuts off prefixes and/or word endings for common ones.
# df["Description"] = df["Description"].apply(lambda x: MyData.word_stemmer(x))
print(df.info())