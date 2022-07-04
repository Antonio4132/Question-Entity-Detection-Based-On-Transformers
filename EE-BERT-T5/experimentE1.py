#!/usr/bin/env python

import re
import sys
from pathlib import Path
import pandas as pd

m = sys.argv[1]
fine_tune = sys.argv[2]

questions = pd.read_csv('QuestionsDataSet.csv')
grouped = questions.groupby('Label')

entities = []

for name, group in grouped:
    entity = name.replace("+"," ")
    entities.append(entity)



len(entities)

from sentence_transformers import SentenceTransformer,  LoggingHandler, losses, models, util

if m == "t5":
  model_name = 't5-small'
else:
  model_name = 'bert-base-uncased'

if fine_tune != "yes":
  word_embedding_model = models.Transformer(model_name)

  pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)

  model = SentenceTransformer(modules=[word_embedding_model, pooling_model])
else:
  model = SentenceTransformer('tsdae-model/')



#Data struture for embeddings of entities
entitiesEmbs = dict()
for e in entities:
  emb = model.encode(sentences=[e])
  entitiesEmbs[e] = emb


from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
import numpy as np


indexesTop1stat = 0
indexesTop3stat = 0
indexesTop5stat = 0
first = True


def algorithm(name,group):
  indexesTop1stat = 0
  indexesTop3stat = 0
  indexesTop5stat = 0
  first = True
  indexesTop1 = []
  indexesTop3 = []
  indexesTop5 = []
  diffs = []
  count = 0
  for i, row in group.iterrows():
    #print(str(i) + " de " + str(group.shape[0]))
    q = row['Question']
    label = row['Label'].replace('+', ' ')
    emb = model.encode(sentences=[q])
    results = dict()
    for e in entitiesEmbs.keys():
      A=np.array(model.encode(sentences=[q]))
      B=np.array(entitiesEmbs[e])
      result=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
      results[e] = result
    diffs.append(results[label])
    maxes = sorted(results, key=results.get, reverse=True)
    if label in maxes[:1]:
      indexesTop1.append(i)
    if label in maxes[:3]:
      indexesTop3.append(i)
    if label in maxes[:5]:
      indexesTop5.append(i)
    
    if count == 1000:
      break

    count = count + 1

  if first:
    indexesTop1stat = len(indexesTop1)/group.shape[0] 
    indexesTop3stat = len(indexesTop3)/group.shape[0]
    indexesTop5stat = len(indexesTop5)/group.shape[0]
    first = False
  else:
    indexesTop1stat = (len(indexesTop1)/group.shape[0] + indexesTop1stat)/2
    indexesTop3stat = (len(indexesTop3)/group.shape[0] + indexesTop3stat)/2
    indexesTop5stat = (len(indexesTop5)/group.shape[0] + indexesTop5stat)/2

  return [name, indexesTop1stat, indexesTop3stat, indexesTop5stat, diffs]

def algorithmFilter(name,group):
  indexes = []
  count = 0
  for i, row in group.iterrows():
    #print(str(i) + " de " + str(group.shape[0]))
    q = row['Question']
    label = row['Label'].replace('+', ' ')
    emb = model.encode(sentences=[q])
    A=np.array(model.encode(sentences=[q]))
    B=np.array(entitiesEmbs[label])
    result=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))

    if not (mean - st_error2 <= result <= mean + st_error2):
      indexes.append(i)

    if count == 2000:
      break

    count = count + 1

  return indexes

results = []

for name, group in grouped:
   a = algorithm(name,group)
   print(a)
   results.append(a)

f = open("resultadosE1.txt", "w")
for r in results:
  for elem in range(0,len(r)-1):
    f.write(str(r[elem]))
    f.write(" ")
  f.write('\n')

f.write("\nMeans:\n\n")

m1 = []
m2 = []
m3 = []

for r in results:
  m1.append(r[1])
  m2.append(r[2])
  m3.append(r[3])

f.write(str(np.mean(m1)) + " " + str(np.mean(m2)) + " " + str(np.mean(m3)))

import math

f.write("\n\nFiltered\n\n")

c = 0
results2 = []
for name, group in grouped:

   distribution = results[c][4]
   mean = np.mean(distribution)
   st_error2 = (np.std(distribution) / math.sqrt(len(distribution)))*2
   indexes = algorithmFilter(name,group)
   groupF = group.drop(indexes, axis=0)
   b = algorithm(name,groupF)
   results2.append(b)
   c += 1

for r in results2:
  for elem in range(0,len(r)-1):
    f.write(str(r[elem]))
    f.write(" ")
  f.write('\n')

f.write("\nMeans:\n\n")

m1 = []
m2 = []
m3 = []

for r in results2:
  m1.append(r[1])
  m2.append(r[2])
  m3.append(r[3])

f.write(str(np.mean(m1)) + " " + str(np.mean(m2)) + " " + str(np.mean(m3)))

f.close()

print("m: " + m)
print("\nfine_tune? " + fine_tune)