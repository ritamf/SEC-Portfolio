from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords



lemmatizer= WordNetLemmatizer()
stop_words=set(stopwords.words('english'))
print(stop_words)

f = open('paperScraping.csv','r')

paperInfo={}

for l in f:
    conteudo=l.split('|')

    if len(conteudo)==4:
        paperInfo[conteudo[1]]={} # articles[title] = dict()
        paperInfo[conteudo[1]]['abstract']=conteudo[3].strip('\n') # articles[title][abstract] = abstract
        paperInfo[conteudo[1]]['ncit']=conteudo[2] # articles[title][ncits] = [ncits]
        # print(paperInfo[conteudo[1]])

f.close()

wordsFreq={}
for paper in paperInfo:
    #print(paper)
    paperInfo[paper]['words']=[]
    text=paperInfo[paper]['abstract'] # texto de abstract de paper aqui
    words=text.split(' ') # abstract = [list of words from abstract]
    #print(words)
    for i in range(len(words)):
        words[i]=words[i].strip(".,()º -") # remove caracteres estranhos de todas as palavras do abstract
        words[i]=words[i].lower() # todas as palavras tao em minusculas
        words[i]=lemmatizer.lemmatize(words[i]) # associa cada palavra a um sinonimo comum 
        if words[i] not in stop_words: # stop words sao excluidas aqui
            if words[i] in wordsFreq:
                wordsFreq[words[i]]+=1
            else:
                wordsFreq[words[i]]=1
            paperInfo[paper]['words'].append(words[i]) # acrescenta se word à lista de palavras
    #print(words)

wordsFreq=dict(sorted(wordsFreq.items(), key=lambda item: item[1])) # ordena dicionario {palavra: freqPalavra} pela freqPalavras
print(wordsFreq)

mostFreq5 = list(wordsFreq.keys())[-200:]

# semelhante mas para freq relativa

percent={}
total_words=len(wordsFreq.keys())
print(mostFreq5)
for paper in paperInfo:
    count=0
    for word in paperInfo[paper]['words']:
        if word in mostFreq5:
            count+=1
    percent[paper]=(count/len(mostFreq5))*100
percent=dict(sorted(percent.items(), key=lambda item: item[1]))
#print(percent)

#print(paperInfo['Rain attenuation for 5G network in tropical region (Malaysia) for terrestrial link']['words'])
