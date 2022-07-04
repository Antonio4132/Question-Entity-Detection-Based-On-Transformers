#!/usr/bin/env python

import owlready2
import re
import sys
from pathlib import Path

onto = owlready2.get_ontology(sys.argv[1]).load()
dir = sys.argv[2]

species = []

for i in onto["Specie"].instances():
    specie = re.findall('[A-Z][^A-Z]*', i.name)
    s = "+"
    s = s.join(specie)
    species.append(s)

for s in species:
    file_name = dir + "/" + s 
    fle = Path(file_name)
    fle.touch(exist_ok=True)

sp = '-'.join([str(item) for item in species])
print(sp)
