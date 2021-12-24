import re
import csv

import pandas as pd
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

from mymodules.myfunctions import display_topics


def mynlp(word):
    # does stemming of the word and checks if that word is a substring of the most common lemmitized word: 
    # if so, returns lemmitized string; else, returns stemmed word
    stem = SnowballStemmer(language='english')
    stemWord = stem.stem(word)
    lemKeys = numLemWordsAllArts.keys()
    
    for lk in lemKeys:
        if stemWord in lk: # se stem word for subpalavra da lem word mais frequente
            return lk

    return stemWord


abstractsWords = [["played","plays","plays","playing","played","elasticity"],["elasticity","elastic"]]
print(abstractsWords)

stop_words = set(stopwords.words('english')) | {""} # used in lemmatization and stemming


### LEMMATIZATION ###

lem = WordNetLemmatizer()
lemAbstractsWords = [[lem.lemmatize(word) for word in abstract if word not in stop_words] for abstract in abstractsWords]

## Frequencia absoluta das palavras lemmitized de TODOS os artigos, em ordem decrescente
flatLemWords = [word for paw in lemAbstractsWords for word in paw]
numLemWordsAllArts = dict(Counter(flatLemWords)) 
numLemWordsAllArts = dict(sorted(numLemWordsAllArts.items(), key=lambda item: item[1])[::-1])
# print(numLemWordsAllArts)


### STEMMING + LEMMATIZATION ###

stemLemAbstractsWords = [[mynlp(word) for word in abstract if word not in stop_words] for abstract in abstractsWords]
print(stemLemAbstractsWords)