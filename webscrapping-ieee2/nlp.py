from numpy import fabs
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

import re

import pandas as pd
from collections import Counter

import csv

search_term = "multi agent systems"

df = pd.read_csv("multi agent systems.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

abstractsWords = [abstract.split(" ") for abstract in abstracts]

lemmatizer= WordNetLemmatizer()
stop_words=set(stopwords.words('english')) | {""}

lemminizedAbstractsWords = [[lemmatizer.lemmatize(word) for word in abstract if lemmatizer.lemmatize(word) not in stop_words] for abstract in abstractsWords]

numWordsEachArt = [dict(Counter(words)) for words in lemminizedAbstractsWords]

## Frequencia absoluta, em ordem decrescente
flatLemminizedAbstractsWords = [word for law in lemminizedAbstractsWords for word in law]
numWordsAllArts = dict(Counter(flatLemminizedAbstractsWords)) 
numWordsAllArts = dict(sorted(numWordsAllArts.items(), key=lambda item: item[1])[::-1])
print(numWordsAllArts)

## Escrever frequencia absoluta num ficheiro csv
with open(f"{search_term}_freqAbs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "counter"])
    for key, value in numWordsAllArts.items():
        writer.writerow([key, value])

## Frequencia relativa em relação ao total de palavras, em ordem decrescente
totalWords = sum(numWordsAllArts.values())
numWordsAllArtsRel = {k : round(v/totalWords*100,5) for k,v in numWordsAllArts.items()}
numWordsAllArtsRel = dict(sorted(numWordsAllArtsRel.items(), key=lambda item: item[1])[::-1])

## Escrever frequencia relativa em relação ao total de palavras num ficheiro csv
with open(f"{search_term}_freqRel.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "counter"])
    for key, value in numWordsAllArtsRel.items():
        writer.writerow([key, value])