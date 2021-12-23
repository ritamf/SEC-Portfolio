import re
import csv

import pandas as pd
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF

from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

def display_topics(model, feature_names, num_top_words, topic_names=None):
    # iterate through topics in topic-term matrix, 'H' aka
    # model.components_
    for ix, topic in enumerate(model.components_):
        #print topic, topic number, and top words
        if not topic_names or not topic_names[ix]:
            print("\nTopic ", ix)
        else:
            print("\nTopic: '",topic_names[ix],"'")
        print(", ".join([feature_names[i] \
             for i in topic.argsort()[:-num_top_words - 1:-1]]))


theme = "multi agent systems"

df = pd.read_csv(f"datasets/{theme}.csv", delimiter="|")
dfAbstracts = df[['abstract']]

abstracts = [re.sub('[^a-zA-Z0-9 \n\.]', ' ', str(abstract[0]).lower()).replace("."," ") for abstract in dfAbstracts.values.tolist()]

abstractsWords = [abstract.split(" ") for abstract in abstracts]

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english')) | {""}

lemminizedAbstractsWords = [[lemmatizer.lemmatize(word) for word in abstract if lemmatizer.lemmatize(word) not in stop_words] for abstract in abstractsWords]

## Frequencia absoluta das palavras de CADA artigo: [{word1: count1, word2:count2,...}, {...}, ...]
numWordsEachArt = [dict(Counter(words)) for words in lemminizedAbstractsWords]
numWordsEachArt = [dict(sorted(d.items(), key=lambda item:item[1])[::-1]) for d in numWordsEachArt]

artNums = [artNum[0] for artNum in df[['art_num']].values.tolist()]

artNumWordsPerArt = list(zip(artNums, numWordsEachArt)) # [(num_art1, {word1:num1, word2:num2,...}),...]

with open(f"datasets/{theme}_freqAbsEach.csv","w") as file:
    writer=csv.writer(file)
    writer.writerow(("num_art", "art_words"))
    for value,item in artNumWordsPerArt:
        writer.writerow((value,item))

wordsPerArt = list(zip(artNums, [" ".join(list(d.keys())) for d in numWordsEachArt])) # [(num_art, word1+" "+word2+" "+...),...] # sem repeticao de palavras no mesmo artigo
# wordsPerArt = list(zip(artNums, [" ".join([k]*v) for words in numWordsEachArt for k,v in words.items()])) # com repeticao de palavras no mesmo artigo: resultados meh

dfWordsPerArt = pd.DataFrame(wordsPerArt, columns =['num_art', 'words'])
print(dfWordsPerArt.head()) 

# Store TF-IDF Vectorizer
tv_noun = TfidfVectorizer(stop_words=stop_words, ngram_range = (1,1), max_df = .8, min_df = .01)

# Fit and Transform speech noun text to a TF-IDF Doc-Term Matrix
data_tv_noun = tv_noun.fit_transform(dfWordsPerArt.words)

# Create data-frame of Doc-Term Matrix with nouns as column names
data_dtm_noun = pd.DataFrame(data_tv_noun.toarray(), columns=tv_noun.get_feature_names_out())

# Set Article's Names as Index
data_dtm_noun.index = df.index

# Visually inspect Document Term Matrix
print(data_dtm_noun.head())

nmf_model = NMF(8)
doc_topic = nmf_model.fit_transform(data_dtm_noun)
display_topics(nmf_model, tv_noun.get_feature_names(), 5)


# ## Frequencia absoluta das palavras de TODOS os artigos, em ordem decrescente
# flatLemminizedAbstractsWords = [word for law in lemminizedAbstractsWords for word in law]
# numWordsAllArts = dict(Counter(flatLemminizedAbstractsWords)) 
# numWordsAllArts = dict(sorted(numWordsAllArts.items(), key=lambda item: item[1])[::-1])
# # print(numWordsAllArts)

# ## Escrever frequencia absoluta das palavras de TODOS os artigos, em ordem decrescente, num ficheiro csv
# with open(f"datasets/{theme}_freqAbs.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerow(["word", "counter"])
#     for key, value in numWordsAllArts.items():
#         writer.writerow([key, value])

# ## Frequencia relativa em relação ao total de palavras, em ordem decrescente
# totalWords = sum(numWordsAllArts.values())
# numWordsAllArtsRel = {k : round(v/totalWords*100,5) for k,v in numWordsAllArts.items()}
# numWordsAllArtsRel = dict(sorted(numWordsAllArtsRel.items(), key=lambda item: item[1])[::-1])

# ## Escrever frequencia relativa em relação ao total de palavras, em ordem decrescente, num ficheiro csv
# with open(f"datasets/{theme}_freqRel.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerow(["word", "freqRel"])
#     for key, value in numWordsAllArtsRel.items():
#         writer.writerow([key, value])