from owlready2 import *
from owlready2 import get_ontology
import pandas as pd

#------------ Ontologia ------------#

df = pd.read_csv("questions_ents.csv")

onto = get_ontology("out_repositoriev6.owl").load()
examples = []

questions = pd.DataFrame()
qs = []
sps = []
phs = []

for index, row in df.iterrows():

    print("New Questions: ")

    relations = onto["SPR.hasDisease"].get_relations()
    for relation in relations:
        newDisease = str(relation[1]).split(".")[1]
        instance = relation[0]
        relations2 = onto["SPR.hasSpecie"].get_relations()
        for r in relations2:
            if r[0] == instance:
                newPopulation = str(r[1]).split(".")[1]
                newQ = row['template'].replace("PHENOTYPE",newDisease).replace("SPECIE", newPopulation)
                if  newQ not in qs:
                    qs.append(newQ)
                    sps.append(newPopulation)
                    phs.append(newDisease)


questions['question'] = qs
questions['specie'] = sps
questions['phenotype'] = phs
questions = questions.drop_duplicates()

questions.to_csv('finalQuestions.csv',index = False)



