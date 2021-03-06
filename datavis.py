import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

theme = "multi agent systems"

df = pd.read_csv(f"datasets/{theme}.csv", delimiter="|")
print(df.info())


### remove rows with no abstract
df = df.dropna()
print(df.info())


### Count number of articles of each type

dfType = df['type'].value_counts()

### Uncomment to save plot of number of articles of each type
# axType = dfType.plot.bar(title="Number of articles of each type", rot=15, figsize=(7,7))
# for p in axType.patches:
#     axType.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
# plt.savefig('plots/num_arts_each_type.png')


### Count number of articles of each year

dfYear = df['year'].value_counts()[::-1]
print(type(dfYear))

### Uncomment to save plot of number of articles of each year
# axYear = dfYear.plot.bar(title="Number of articles of each year", rot=45, figsize=(8,9))
# for p in axYear.patches:
#     axYear.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 13),  rotation=90, textcoords='offset points')
# plt.savefig('plots/num_arts_each_year.png')


### Stats for number of downloads of each type

dfTypeNumDwnlds = df[['type', 'num_dwnlds']]

dfTypeNumDwnlds = dfTypeNumDwnlds.groupby('type').aggregate([sum, np.average])


### Sum of downloads of each type
dfTypeNumDwnldsSum = dfTypeNumDwnlds[('num_dwnlds', 'sum')]

### Uncomment to save plot of sum of downloads of each type
# axSum = dfTypeNumDwnldsSum.plot.bar(title="Sum of number of downloads per type of paper", rot=15, figsize=(8,8))
# for p in axSum.patches:
#     axSum.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
# plt.savefig('plots/num_dwnlds_sum.png')


### Average number of downloads of each type
dfTypeNumDwnldsAvg = dfTypeNumDwnlds[('num_dwnlds', 'average')]

### Uncomment to save plot of avegrage of downloads of each type
# axAvg = dfTypeNumDwnldsAvg.plot.bar(title="Average number of downloads per type of paper", rot=15, figsize=(7,7))
# for p in axAvg.patches:
#     axAvg.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
# plt.savefig('plots/num_dwnlds_avg.png')


### Stats for number of citations of each type

dfTypeNumCits = df[['type', 'num_cits']]

dfTypeNumCits = dfTypeNumCits.groupby('type').aggregate([sum, np.average])


### Sum of citations of each type
dfTypeNumCitsSum = dfTypeNumCits[('num_cits', 'sum')]

### Uncomment to save plot of sum number of citations of each type
# axSum = dfTypeNumCitsSum.plot.bar(title="Sum of number of citations per type of paper", rot=15, figsize=(6,6))
# for p in axSum.patches:
#     axSum.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
# plt.savefig('plots/num_cits_sum.png')


### Average number of citations of each type
dfTypeNumCitsAvg = dfTypeNumCits[('num_cits', 'average')]

### Uncomment to save plot of average number of citations of each type
# axAvg = dfTypeNumCitsAvg.plot.bar(title="Average number of citations per type of paper", rot=15, figsize=(7,7))
# for p in axAvg.patches:
#     axAvg.annotate(np.round(p.get_height(),decimals=2), (p.get_x()+p.get_width()/2., p.get_height()), ha='center', va='center', xytext=(0, 5), textcoords='offset points')
# plt.savefig('plots/num_cits_avg.png')
