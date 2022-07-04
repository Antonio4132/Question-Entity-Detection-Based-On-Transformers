import pandas as pd
import stanza
from owlready2 import *
from owlready2 import get_ontology
import sys

def parse(text):
        text = str(text)
        text = text.split('.')
        return text[1]

def parseName(text):
        words_list = re.findall('[A-Z][^A-Z]*', parse(text))
        return " ".join(words_list)

def parseAction(text):
        text = parse(text)
        words_list = re.findall('[A-Za-z][^A-Z]*', text)
        action = list()
        action.append(words_list[0])
        del words_list[0]
        del words_list[-1]
        action.append(" ".join(words_list))
        return action

    #stanza.download('en') # download English model
    #stanza.download('en', package='mimic', processors={'ner': 'i2b2'})
#stanza.download('en', package='mimic', processors={'ner': 'BioNLP13CG'})
#stanza.download('en', package='mimic', processors={'ner': 'ncbi_disease'})

nlpPOP = stanza.Pipeline('en', package='mimic', processors={'ner': 'BioNLP13CG'})

nlpDIS = stanza.Pipeline('en', package='mimic', processors={'ner': 'ncbi_disease'})


qBase = pd.read_csv(sys.argv[1])

df = pd.DataFrame()
df['question'] = qBase["question"]
pops = []
diss = []

for index, row in qBase.iterrows():
    docPop = nlpPOP(row['question']) # run annotation over a sentence
    docDis = nlpDIS(row['question']) # run annotation over a sentence

    population = "EMPTY"
    disease = "EMPTY"

    for ent in docPop.entities:
        if (ent.type == "ORGANISM"):
            population = ent.text
        
    for ent in docDis.entities:
        if (ent.type == "DISEASE"):
            disease = ent.text
        
    print(row['question'])
    if population != "":
        print("Population:\t" + population)   
    
    if disease != "":
        print("Disease:\t" + disease)

    pops.append(population)
    diss.append(disease)

    
df['Specie'] = pops
df['Phenotype'] = diss

print(df)

countSp = df['Specie'].value_counts()
spPctg = 100 - (countSp.EMPTY/df['Specie'].size * 100)
print("Percentage of species detected: " + str(spPctg))

countSp = df['Phenotype'].value_counts()
spPctg = 100 - (countSp.EMPTY/df['Phenotype'].size * 100)
print("Percentage of phenotypes detected: " + str(spPctg))

df['Phenotype']

df.to_csv("questions.csv",index=False)