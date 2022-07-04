import glob, os
import pandas as pd
import sys

first  = True
data = {
            'Question': [],
            'Label': []
        }
df = pd.DataFrame(data)

for file in glob.glob("*.csv"):
    if first:
        data = {
            'Question': [],
            'Label': []
        }
        df = pd.DataFrame(data)
        first = False

    questionsDF = pd.read_csv(file)
    df = df.append(questionsDF)

df = df.sample(frac=1)

df.to_csv("QuestionsDataSet.csv", index=False)

sys.stdout = open('Measures.txt', 'a+')

print("Medidas de Calidad del DataSet de Preguntas:")


print("Numero de Preguntas: " + str(df.shape[0]))

for name in df['Label'].unique():
  print("Especie " + name + ": " + str(df.loc[df["Label"] == name].shape[0]) + ".")

for name in df['Label'].unique():
  names = name.split("+")
  explicits = 0
  implicits = 0
  for r in df.loc[df["Label"] == name].Question:
    exp = False
    for n in names:
      if n in r:
        exp = True
    if exp:
      explicits +=1
    else:
      implicits +=1
  specieTotal = df.loc[df["Label"] == name].shape[0]
  print("Especie " + name + ": Explicitos -> " + str(explicits) + " (" + "{:.2f}".format(explicits/specieTotal) + ")" + " Implicitos: " + str(implicits) + " (" + "{:.2f}".format(implicits/specieTotal) + ")")


#from gensim.test.utils import common_texts
#from gensim.models import Word2Vec

#sentences = list(df['Question'])
#splitted_sentences = []
#for s in sentences:
#  splitted_sentences.append(s.lower().replace('?','').split(" "))

#model = Word2Vec(sentences=splitted_sentences, vector_size=10, window=5, min_count=1, workers=4)

#model.wv.key_to_index.keys()
#results = []
#for s1 in splitted_sentences:
#  for s2 in splitted_sentences:
#    results.append(model.wv.wmdistance(s1, s2))

#avg = sum(results)/len(results)
#print("Heterogeniedad del dataset: ", avg)

import os
size = os.path.getsize("QuestionsDataSet.csv")

print("DataSet File Size: " + str(size) + " bytes.")

sys.stdout.close()