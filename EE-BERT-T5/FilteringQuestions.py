from sentence_transformers import SentenceTransformer,  LoggingHandler, losses, models, util
import pandas as pd
import os.path
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
import numpy as np


model = SentenceTransformer('pritamdeka/S-Biomed-Roberta-snli-multinli-stsb')


if True:
    questions = pd.read_csv("QuestionsPhenotypeNew.csv")
    grouped = questions.groupby('Label')
    entitiesEmbs = dict()
    for name, group in grouped: 
        emb = model.encode(sentences=[name.replace("+"," ")])
        entitiesEmbs[name] = emb[0]

    print("Creating Embs...")

    similarityToLabel = []
    for index, row in questions.iterrows():
        A=np.array(model.encode(sentences=[row.Question]))
        B=np.array(entitiesEmbs[row.Label])
        result=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
        similarityToLabel.append(result)

    print("Done.")
    questions['similarityToLabel'] = similarityToLabel

    questions.to_csv("QuestionsPhenotypeFilterNew.csv")
