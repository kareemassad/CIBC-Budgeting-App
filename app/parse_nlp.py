# Import packages and modules
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


# friends speech
part1 = """We are gathered here today on this joyous occasion to celebrate the special love that Monica and Chandler share.
It is a love based on giving and receiving as well as having and sharing. And the love that they give and have is shared and received. 
And through this having and giving and sharing and receiving, we too can share and love and have... and receive."""
part2 = """When I think of the love these two givers and receivers share I cannot help but envy the lifetime ahead of having and 
loving and giving and receiving."""

# Create a dataframe
X_train = pd.DataFrame([part1, part2], columns=["speech"])
print(X_train)

# test processing
def preprocess_text(text):
    # Tokenise words while ignoring punctuation
    tokeniser = RegexpTokenizer(r"\w+")
    tokens = tokeniser.tokenize(text)

    # Lowercase and lemmatise
    lemmatiser = WordNetLemmatizer()
    lemmas = [lemmatiser.lemmatize(token.lower(), pos="v") for token in tokens]
    # Remove stopwords
    keywords = [lemma for lemma in lemmas if lemma not in stopwords.words("english")]
    return keywords


# Create an instance of TfidfVectorizer
vectoriser = TfidfVectorizer(analyzer=preprocess_text)
# Fit to the data and transform to feature matrix
X_train = vectoriser.fit_transform(X_train["speech"])
# Convert sparse matrix to dataframe
X_train = pd.DataFrame.sparse.from_spmatrix(X_train)
# Save mapping on which index refers to which words
col_map = {v: k for k, v in vectoriser.vocabulary_.items()}
# Rename each column using the mapping
for col in X_train.columns:
    X_train.rename(columns={col: col_map[col]}, inplace=True)
print(X_train)