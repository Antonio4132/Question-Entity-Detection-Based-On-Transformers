

import sys
import transformers
import pandas as pd
import os
import nltk
import ntpath

nltk.download('punkt')

if len(sys.argv) == 3:
  df = pd.read_csv(sys.argv[1] + "/" + sys.argv[2])
else:
  species=""

  for i in  range(2,len(sys.argv)):
    specie = ntpath.basename(sys.argv[i])
    species += specie

  df = pd.read_csv(sys.argv[1] + "/" + species + ".csv")


from pipelines import pipeline
#nlp = pipeline("e2e-qg", model="valhalla/t5-base-e2e-qg")
nlp = pipeline("e2e-qg")

questions = []
labels = []

print("Number of Abstracts: " + str(df.shape[0]))
print("Creating Questions...")

grouped = df.groupby('Label')

for name, group in grouped:
  for i in range(0,group.shape[0]):
    sentence = group.iloc[i]['Body'].values[0].replace('\n',' ')
    label = group.iloc[i]['Label']
    qs = nlp(sentence)
    for q in qs:
      questions.append(q)
      labels.append(label)
    print(i)

print("Done.")

data = {
  'Question': questions,
  'Label': labels
}
questionsDF = pd.DataFrame(data)

if len(sys.argv) == 3:
  questionsDF.to_csv("questions" + sys.argv[2], index=False)
else:
  questionsDF.to_csv("questions" + species + ".csv", index=False)
