from nltk.corpus import stopwords

# the words contained in this set will not be processed
mystopwords = set(stopwords.words('english'))
mystopwords = mystopwords | {"", "multi", "agent", "agents", "system", "systems", "mas"}
mystopwords = mystopwords | {"paper", "throughout", "finally", "moreover", "used", "example"}