from numpy import fabs
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

import re

import pandas as pd
from collections import Counter

import csv

theme = "dummySample"

df = pd.read_csv(f"{theme}.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

abstractsWords = [abstract.split(" ") for abstract in abstracts]

lemmatizer= WordNetLemmatizer()
stop_words=set(stopwords.words('english')) | {""}

lemminizedAbstractsWords = [[lemmatizer.lemmatize(word) for word in abstract if lemmatizer.lemmatize(word) not in stop_words] for abstract in abstractsWords]

# Usado tanto para freq das palavras de cada abstract (apenas em amostras de datasets), como para freq de palavras total nos abstracts
flatLemminizedAbstractsWords = [word for law in lemminizedAbstractsWords for word in law]

## Frequencia absoluta das palavras de cada artigo
setAllWords = set(flatLemminizedAbstractsWords)
numWordsEachArt = [dict(Counter(words)) | {word:0 for word in setAllWords if word not in dict(Counter(words)).keys()} for words in lemminizedAbstractsWords] 
print(numWordsEachArt)

# with open(f'{theme}_freqAbsEach.csv', 'w', newline='') as output_file: # é preciso de comentar para datasets grandes
#     keys = numWordsEachArt[0].keys()
#     dict_writer = csv.DictWriter(output_file, keys)
#     dict_writer.writeheader()
#     dict_writer.writerows(numWordsEachArt)

## Frequencia absoluta das palavras de todos os artigos, em ordem decrescente
numWordsAllArts = dict(Counter(flatLemminizedAbstractsWords)) 
numWordsAllArts = dict(sorted(numWordsAllArts.items(), key=lambda item: item[1])[::-1])
print(numWordsAllArts)

## Escrever frequencia absoluta das palavras de todos os artigos, em ordem decrescente, num ficheiro csv
with open(f"{theme}_freqAbs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "counter"])
    for key, value in numWordsAllArts.items():
        writer.writerow([key, value])

## Frequencia relativa em relação ao total de palavras, em ordem decrescente
totalWords = sum(numWordsAllArts.values())
numWordsAllArtsRel = {k : round(v/totalWords*100,5) for k,v in numWordsAllArts.items()}
numWordsAllArtsRel = dict(sorted(numWordsAllArtsRel.items(), key=lambda item: item[1])[::-1])

## Escrever frequencia relativa em relação ao total de palavras, em ordem decrescente, num ficheiro csv
with open(f"{theme}_freqRel.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "freqRel"])
    for key, value in numWordsAllArtsRel.items():
        writer.writerow([key, value])