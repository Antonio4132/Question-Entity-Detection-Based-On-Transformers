

import sys
import transformers
import pandas as pd
import os
import nltk
import ntpath

nltk.download('punkt')

import glob

csvs = glob.glob(sys.argv[1] + "/" + '*.csv')

df = pd.read_csv(csvs[0])


from pipelines import pipeline
#nlp = pipeline("e2e-qg", model="valhalla/t5-base-e2e-qg")
nlp = pipeline("e2e-qg")
#nlp = pipeline("multitask-qa-qg", model="valhalla/t5-base-qa-qg-hl")

questions = []
labels = []

print("Number of Abstracts: " + str(df.shape[0]))
print("Creating Questions...")

grouped = df.groupby('Label')


for index, group in grouped:
  c = 0
  for i,row in group.iterrows():
    sentence = row['Body']
    label = row['Label']
    qs = nlp(sentence)
    for q in qs:
      questions.append(q)
      labels.append(label)
    
    if c == 1000:
      break
    if c % 100 == 0:
      print(c)
    c += 1

  print("%s %d" % (index,c))

print("Done.")

data = {
  'Question': questions,
  'Label': labels
}
questionsDF = pd.DataFrame(data)

if len(sys.argv) == 3:
  questionsDF.to_csv("questions" + sys.argv[2], index=False)
else:
  questionsDF.to_csv("questions" + ".csv", index=False)
