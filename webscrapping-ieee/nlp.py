from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords

import json

lemmatizer= WordNetLemmatizer()

stop_words=set(stopwords.words('english'))

with open('multi_agent_systems.json') as f:
    json_content = json.load(f)

