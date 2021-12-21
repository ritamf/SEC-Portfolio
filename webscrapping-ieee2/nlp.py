from numpy import fabs
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

import re

import pandas as pd
from collections import Counter

df = pd.read_csv("dummySample.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', '', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

abstractsWords = [abstract.split(" ") for abstract in abstracts]

lemmatizer= WordNetLemmatizer()
stop_words=set(stopwords.words('english')) | {""}

lemminizedAbstractsWords = [[lemmatizer.lemmatize(word) for word in abstract if lemmatizer.lemmatize(word) not in stop_words] for abstract in abstractsWords]

numWordsEachArt = [dict(Counter(words)) for words in lemminizedAbstractsWords]
print(sum([sum(d.values()) for d in numWordsEachArt]))

## Frequencia absoluta, em ordem decrescente
flatLemminizedAbstractsWords = [word for abstractWords in lemminizedAbstractsWords for word in abstractWords]
numWordsAllArts = dict(Counter(flatLemminizedAbstractsWords)) 
numWordsAllArts = dict(sorted(numWordsAllArts.items(), key=lambda item: item[1])[::-1])

## Frequencia relativa, em ordem decrescente
totalWords = sum(numWordsAllArts.values())
numWordsAllArtsRel = {k : round(v/totalWords*100,3) for k,v in numWordsAllArts.items()}
numWordsAllArtsRel = dict(sorted(numWordsAllArtsRel.items(), key=lambda item: item[1])[::-1])
print(numWordsAllArtsRel)