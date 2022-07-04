from collections import Counter

from numpy import log10
import pandas as pd
import plotly
import plotly.graph_objs as go
import plotly.express as px
import umap
from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
from plotly.graph_objs import *

from sentence_transformers import SentenceTransformer,  LoggingHandler, losses, models, util

questions = pd.read_csv("QuestionsDatasetREDUCED.csv")
grouped = questions.groupby('Label')

entities = []

for name, group in grouped:
    entity = name.replace("+"," ")
    entities.append(entity)

'''model_name = 'bert-base-uncased'
model = SentenceTransformer('tsdae-model/')
word_embedding_model = models.Transformer(model_name)

pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)

model = SentenceTransformer(modules=[word_embedding_model, pooling_model])'''

model = SentenceTransformer('pritamdeka/S-Biomed-Roberta-snli-multinli-stsb')

#Data struture for embeddings of entities
entitiesEmbs = dict()
for e in entities:
  emb = model.encode(sentences=[e])
  entitiesEmbs[e] = emb[0]

questionsDict = dict()

for label, group in grouped:
  qd = dict()
  c = 0
  for index, row in group.iterrows():
    emb = model.encode(sentences=[row.Question])
    qd[row.Question] = emb[0]
    c += 1
    if c == 1000:
      break
  print("%s terminada!" % label)
  questionsDict[label] = qd

entsDf = pd.DataFrame.from_dict(entitiesEmbs, orient='index')

texto = entsDf.index.to_list()
tipo = entsDf.index.to_list()
categoria = ['entity'] * len(tipo) 
size = [100] * len(tipo) 

for label in questionsDict.keys():
  d = pd.DataFrame.from_dict(questionsDict[label], orient='index')
  entsDf = pd.concat([entsDf,d])
  indexes = d.index.to_list()
  texto += indexes
  tipo += [label.replace("+"," ")] * len(indexes)
  categoria += ['question'] * len(indexes)
  size += [10] * len(indexes)

reducer = umap.UMAP(metric='cosine', n_neighbors=15, min_dist=0.05, random_state=42)

embedding = reducer.fit_transform(entsDf)

d = pd.DataFrame(embedding, columns=['c1', 'c2'])

d['categoria'] = categoria
d['tipo'] = tipo
d['texto'] = texto
d['s'] = size

print(d.head())

ent = 'Specie'
ma = '_MA'


filename = "UMAP_" + ent + 'Filter' + ma + ".html"
#d[prop] = listForProperty(d['project'], prop, dic)

#d = d.drop(d[d.c2 > 10].index)
#d = d.drop(d[d.c1 > 6].index)

fig = px.scatter(d, x="c1", y="c2",
                 color=d.tipo,
                 hover_data=['texto'],
                 title="UMAP for Phenotype",
                 width=800, height=600,
                 size= d.s,
                 size_max = 20,
                 symbol = d.categoria
)
chart = plotly.offline.plot(fig, filename=filename)