import re
import csv

import pandas as pd
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from time import time

from mymodules.myfunctions import save_plot_top_words


n_samples = 2000
n_features = 1000
n_components = 10
n_top_words = 20


def mynlp(word):
    # does stemming of the word and checks if that word is a substring of the most common lemmitized word: 
    # if so, returns lemmitized string; else, returns stemmed word
    stem = SnowballStemmer(language='english')
    stemWord = stem.stem(word)
    lemKeys = dictLemWordsCounter.keys()
    
    for lk in lemKeys:
        if stemWord in lk: # se stem word for subpalavra da lem word mais frequente
            return lk

    return stemWord


theme = "multi agent systems"

df = pd.read_csv(f"datasets/{theme}.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

lstWordsPerAbs = [abstract.split(" ") for abstract in abstracts]

stop_words = set(stopwords.words('english')) | {"", "multi", "agent", "systems"} # used in lemmatization and stemming

### LEMMATIZATION ###

lem = WordNetLemmatizer()
lstLemWordsPerAbs = [[lem.lemmatize(word) for word in abstract if lem.lemmatize(word) not in stop_words] for abstract in lstWordsPerAbs]

## Frequencia absoluta das palavras lemmitized de TODOS os artigos, em ordem decrescente
lstLemWords = [word for paw in lstLemWordsPerAbs for word in paw]
dictLemWordsCounter = dict(Counter(lstLemWords)) 
dictLemWordsCounter = dict(sorted(dictLemWordsCounter.items(), key=lambda item: item[1])[::-1])
# print(dictLemWordsCounter)

## Escrever frequencia absoluta das palavras lemmitized de TODOS os artigos, em ordem decrescente, num ficheiro csv
with open(f"datasets/{theme}_lemFreqAbs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "counter"])
    for key, value in dictLemWordsCounter.items():
        writer.writerow([key, value])


### STEMMING + LEMMATIZATION ###

lstStemLemWordsPerAbs = [[mynlp(word) for word in abstract if word not in stop_words] for abstract in lstLemWordsPerAbs]

## Frequencia absoluta das palavras stemmed e lemmitized de CADA artigo: [{word1:count1, word2:count2,...}, {...}, ...]
dictStemLemWordsCounter = [dict(Counter(words)) for words in lstStemLemWordsPerAbs]
dictStemLemWordsCounter = [dict(sorted(d.items(), key=lambda item:item[1])[::-1]) for d in dictStemLemWordsCounter]

artNums = [artNum[0] for artNum in df[['art_num']].values.tolist()]

lstArtNumWordsPerArt = list(zip(artNums, dictStemLemWordsCounter)) # [(num_art1, {word1:num1, word2:num2,...}),...]

with open(f"datasets/{theme}_stemLemFreqAbsEach.csv","w") as file:
    writer=csv.writer(file)
    writer.writerow(("num_art", "art_words"))
    for value,item in lstArtNumWordsPerArt:
        writer.writerow((value,item))


### Non-negative Matrix Factorization ###

data_samples = abstracts[:n_samples]
print(data_samples[0])

# print("done in %0.3fs." % (time() - t0))

# Use tf-idf features for NMF.
print("Extracting tf-idf features for NMF...")
tfidf_vectorizer = TfidfVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
)
t0 = time()
tfidf = tfidf_vectorizer.fit_transform(data_samples)
print(tfidf)
print("done in %0.3fs." % (time() - t0))

# Use tf (raw term count) features for LDA.
print("Extracting tf features for LDA...")
tf_vectorizer = CountVectorizer(
    max_df=0.95, min_df=2, max_features=n_features, stop_words="english"
)
t0 = time()
tf = tf_vectorizer.fit_transform(data_samples)
print("done in %0.3fs." % (time() - t0))
print()

# Fit the NMF model (Frobenius norm)
print(
    "Fitting the NMF model (Frobenius norm) with tf-idf features, "
    "n_samples=%d and n_features=%d..." % (n_samples, n_features)
)
t0 = time()
nmf = NMF(n_components=n_components, random_state=1, alpha=0.1, l1_ratio=0.5).fit(tfidf)
print("done in %0.3fs." % (time() - t0))


tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
save_plot_top_words(
    nmf, tfidf_feature_names, n_top_words, "Topics in NMF model (Frobenius norm)"
)

# Fit the NMF model (generalized Kullback-Leibler divergence)
print(
    "\n" * 2,
    "Fitting the NMF model (generalized Kullback-Leibler "
    "divergence) with tf-idf features, n_samples=%d and n_features=%d..."
    % (n_samples, n_features),
)
t0 = time()
nmf = NMF(
    n_components=n_components,
    random_state=1,
    beta_loss="kullback-leibler",
    solver="mu",
    max_iter=1000,
    alpha=0.1,
    l1_ratio=0.5,
).fit(tfidf)
print("done in %0.3fs." % (time() - t0))

tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
save_plot_top_words(
    nmf,
    tfidf_feature_names,
    n_top_words,
    "Topics in NMF model (generalized Kullback-Leibler divergence)",
)

# Topics in LDA model
print(
    "\n" * 2,
    "Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
    % (n_samples, n_features),
)
lda = LatentDirichletAllocation(
    n_components=n_components,
    max_iter=5,
    learning_method="online",
    learning_offset=50.0,
    random_state=0,
)
t0 = time()
lda.fit(tf)
print("done in %0.3fs." % (time() - t0))

tf_feature_names = tf_vectorizer.get_feature_names_out()
save_plot_top_words(lda, tf_feature_names, n_top_words, "Topics in LDA model")
