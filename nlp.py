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


theme = "multi agent systems"

df = pd.read_csv(f"datasets/{theme}.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

abstractsWords = [abstract.split(" ") for abstract in abstracts]

stop_words = set(stopwords.words('english')) | {"", "multi", "agent", "systems"} # used in lemmatization and stemming

### LEMMATIZATION ###

lem = WordNetLemmatizer()
lemAbstractsWords = [[lem.lemmatize(word) for word in abstract if word not in stop_words] for abstract in abstractsWords]

## Frequencia absoluta das palavras lemmitized de TODOS os artigos, em ordem decrescente
flatLemWords = [word for paw in lemAbstractsWords for word in paw]
numLemWordsAllArts = dict(Counter(flatLemWords)) 
numLemWordsAllArts = dict(sorted(numLemWordsAllArts.items(), key=lambda item: item[1])[::-1])
# print(numLemWordsAllArts)

## Escrever frequencia absoluta das palavras lemmitized de TODOS os artigos, em ordem decrescente, num ficheiro csv
with open(f"datasets/{theme}_lemFreqAbs.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["word", "counter"])
    for key, value in numLemWordsAllArts.items():
        writer.writerow([key, value])


### STEMMING + LEMMATIZATION ###

stemLemAbstractsWords = [[mynlp(word) for word in abstract if word not in stop_words] for abstract in abstractsWords]

## Frequencia absoluta das palavras stemmed e lemmitized de CADA artigo: [{word1:count1, word2:count2,...}, {...}, ...]
numWordsEachArt = [dict(Counter(words)) for words in stemLemAbstractsWords]
numWordsEachArt = [dict(sorted(d.items(), key=lambda item:item[1])[::-1]) for d in numWordsEachArt]

artNums = [artNum[0] for artNum in df[['art_num']].values.tolist()]

artNumWordsPerArt = list(zip(artNums, numWordsEachArt)) # [(num_art1, {word1:num1, word2:num2,...}),...]

with open(f"datasets/{theme}_stemLemFreqAbsEach.csv","w") as file:
    writer=csv.writer(file)
    writer.writerow(("num_art", "art_words"))
    for value,item in artNumWordsPerArt:
        writer.writerow((value,item))


### Non-negative Matrix Factorization ###

wordsPerArt = list(zip(artNums, [" ".join(list(d.keys())) for d in numWordsEachArt])) # [(num_art, word1+" "+word2+" "+...),...] # sem repeticao de palavras no mesmo artigo
# wordsPerArt = list(zip(artNums, [" ".join([k]*v) for words in numWordsEachArt for k,v in words.items()])) # com repeticao de palavras no mesmo artigo: resultados meh

dfWordsPerArt = pd.DataFrame(wordsPerArt, columns=['num_art', 'words'])
# print(dfWordsPerArt.head()) 

# Store TF-IDF Vectorizer
tv_noun = TfidfVectorizer(stop_words=stop_words, ngram_range = (1,1), max_df = .8, min_df = .01)
print(tv_noun)

# Fit and Transform speech noun text to a TF-IDF Doc-Term Matrix
data_tv_noun = tv_noun.fit_transform(dfWordsPerArt.words)

# Create data-frame of Doc-Term Matrix with nouns as column names
data_dtm_noun = pd.DataFrame(data_tv_noun.toarray(), columns=tv_noun.get_feature_names_out())

# Set Article's Names as Index
data_dtm_noun.index = df.index

# Visually inspect Document Term Matrix
# print(data_dtm_noun.head())

nmf_model = NMF(8)
doc_topic = nmf_model.fit_transform(data_dtm_noun)
display_topics(nmf_model, tv_noun.get_feature_names(), 5)


# ## Frequencia relativa em relação ao total de palavras, em ordem decrescente
# totalWords = sum(numLemWordsAllArts.values())
# numLemWordsAllArtsRel = {k : round(v/totalWords*100,5) for k,v in numLemWordsAllArts.items()}
# numLemWordsAllArtsRel = dict(sorted(numLemWordsAllArtsRel.items(), key=lambda item: item[1])[::-1])

# ## Escrever frequencia relativa em relação ao total de palavras, em ordem decrescente, num ficheiro csv
# with open(f"datasets/{theme}_lemFreqRel.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerow(["word", "freqRel"])
#     for key, value in numLemWordsAllArtsRel.items():
#         writer.writerow([key, value])