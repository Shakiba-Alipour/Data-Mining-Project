import nltk
import string
import numpy as np
import re
import pandas as pd
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from gensim.parsing.preprocessing import remove_stopwords
from keybert import KeyBERT
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import matplotlib.pyplot as plot
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sentence_transformers import SentenceTransformer

nltk.download("stopwords")
nltk.download('wordnet')
Dataset = pd.read_csv("UT.csv", encoding="ISO-8859-1")
pd.set_option('display.max_colwidth', -1)
Dataset = Dataset[['Objective', 'Language']][1:]
kw_model = KeyBERT()
keywords = []
data = []
keys = []
stopwords = nltk.corpus.stopwords.words('english')
porter_stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()
nltk.download('omw-1.4')


def remove_punctuation(text):
    punctuationfree = ""
    if(text is np.nan):
        return punctuationfree
    for i in range(len(text)):
        if(text[i] not in string.punctuation):
            punctuationfree = punctuationfree + text[i]

    return punctuationfree


def tokenization(text):
    PATTERN = r"\w+"
    tokens = re.findall(PATTERN, text)
    return tokens


def remove_stopwords(text):
    output = [i for i in text if i not in stopwords]
    return output


def stemming(text):
    stem_text = [porter_stemmer.stem(word) for word in text]
    return stem_text


def lemmatizer(text):
    lemm_text = [wordnet_lemmatizer.lemmatize(word) for word in text]
    Dataset.head()
    return lemm_text


def listToString(s):
    str1 = " "
    Dataset.head()
    return (str1.join(s))


# cleaning the data from punctuations and lowerize
Dataset['clean_Objective'] = Dataset['Objective'].apply(
    lambda x: remove_punctuation(x))
Dataset['clean_Language'] = Dataset['Language'].apply(
    lambda x: remove_punctuation(x))
Dataset['clean_Objective'] = Dataset['clean_Objective'].apply(
    lambda x: str(x).lower())
Dataset['clean_Language'] = Dataset['clean_Language'].apply(
    lambda x: str(x).lower())

# tokenize data
Dataset['tokenied_Objective'] = Dataset['clean_Objective'].apply(
    lambda x: tokenization(x))
Dataset['tokenied_Language'] = Dataset['clean_Language'].apply(
    lambda x: tokenization(x))

# remove stopwords
Dataset['tokenied_Objective'] = Dataset['tokenied_Objective'].apply(
    lambda x: remove_stopwords(x))
Dataset['tokenied_Language'] = Dataset['tokenied_Language'].apply(
    lambda x: remove_stopwords(x))

# stemming data
Dataset['stemmed_Objective'] = Dataset['tokenied_Objective'].apply(
    lambda x: stemming(x))
Dataset['stemmed_Language'] = Dataset['tokenied_Language'].apply(
    lambda x: stemming(x))

# lemmatize data
Dataset['lemmatized_Objective'] = Dataset['tokenied_Objective'].apply(
    lambda x: lemmatizer(x))
Dataset['lemmatized_Language'] = Dataset['tokenied_Language'].apply(
    lambda x: lemmatizer(x))

# extract keywords
Dataset['lemmatized_Objective'] = Dataset['lemmatized_Objective'].apply(
    lambda x: listToString(x))
Dataset['lemmatized_Language'] = Dataset['lemmatized_Language'].apply(
    lambda x: listToString(x))

for item in Dataset['lemmatized_Objective']:
    keywords.append(kw_model.extract_keywords(item))
    Dataset['keywords'] = keywords

for item in Dataset['lemmatized_Language']:
    keywords.append(kw_model.extract_keywords(item))

for i in range(1, len(Dataset['keywords'])):
    Dataset['keywords'][i] += keywords[i]

    Dataset.head()

for course in Dataset['keywords']:
    for key in course:
        keys.append(key[0])
    data.append(keys)

# frequent items
te = TransactionEncoder()
te_ary = te.fit(data).transform(data)
df = pd.DataFrame(te_ary, columns=te.columns_)

# association rules
frequent_itemsets = apriori(df, min_support=0.01, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(
    lambda x: len(x))
frequent_itemsets


# Phase 2
# Embedding
outsome_sentences = data['lemmatized_outcome']
description_sentences = data['lemmatized_description']
if 0 not in outsome_sentences:
    outsome_sentences[0] = []
if 0 not in description_sentences:
    description_sentences[0] = []
model = SentenceTransformer('sentence-transformers/bert-base-nli-mean-tokens')
outcome_embeddings = model.encode(outsome_sentences)
description_embeddings = model.encode(description_sentences)


# Clustering
features, labels = make_blobs(
    n_samples=200, centers=3, cluster_std=2.75, random_state=42)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
kmeans = KMeans(init="random", n_clusters=3, n_init=10,
                max_iter=300, random_state=42)
kmeans.fit(scaled_features)
sse = []
for k in range(1, 11):
  kmeans = KMeans(n_clusters=k,random_state=0)
  kmeans.fit(scaled_features)
  sse.append(kmeans.inertia_)

plot.style.use("fivethirtyeight")
plot.plot(range(1, 11), sse)
plot.xticks(range(1, 11))
plot.xlabel("Number of Clusters")
plot.ylabel("SSE")
plot.show()
