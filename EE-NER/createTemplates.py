import pandas as pd
import sys


df = pd.read_csv(sys.argv[1], index_col=False)

templates = []

#------------ Template Creation ------------#
for index, row in df.iterrows():
    template = row['question']

    if str(row["Specie"]) != "":
        template = template.replace(str(row["Specie"]),"SPECIE")
    if str(row["Phenotype"]) != "":
        template = template.replace(str(row["Phenotype"]),"PHENOTYPE")

    templates.append(template)

df['template'] = templates

df.to_csv('questions_ents.csv', index=False)