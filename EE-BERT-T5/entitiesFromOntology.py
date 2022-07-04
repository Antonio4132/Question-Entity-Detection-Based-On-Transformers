#!/usr/bin/env python

import owlready2
import re
import sys
from pathlib import Path
import glob

# Locate Ontology
onto = owlready2.get_ontology(sys.argv[1]).load()
dir = sys.argv[2]
entity = sys.argv[3]

# Look if there are already files y the folder
files = glob.glob(sys.argv[2]+ "/" + '*')

if len(files) < 1:

    entities = []

    # Create a empty file for every instance of the class
    for i in onto[entity].instances():
        entity = re.findall('[A-Z]{2,}[^A-Z]*|[A-Z][^A-Z]*', i.name.replace('+','%2b').replace('/',''))
        s = "+"
        s = s.join(entity)
        entities.append(s)

    for s in entities:
        file_name = dir + "/" + s 
        fle = Path(file_name)
        fle.touch(exist_ok=True)

