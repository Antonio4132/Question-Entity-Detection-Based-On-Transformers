#!/usr/bin/env python

from multiprocessing.connection import wait
import sys
import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re
import time
import ntpath
import random


def getAbstractsfromLabel(label):

  label = re.findall('[A-Z]{2,}[^A-Z]*|[A-Z][^A-Z]*', label.replace('+','').replace('/',''))
  lF = ''
  for l in label:
    lF += l + '[TITL]'
    if l != label[-1]:
      lF += '+AND+'

  #Assemble search query
  baseSearch = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
  db = 'db=pubmed'
  term = 'term=' + lF
  tail = 'retmax=100&usehistory=y'
  email = 'email=antonio.arquesa@gmail.com'

  urlSearch = baseSearch + '&' + db + '&' + term + '&' + tail + '&' + email

  #Get method
  search = requests.get(urlSearch)
  time.sleep(1)


  #Obatin info
  root = ET.fromstring(search.text)
  webEnv = root.find('WebEnv').text
  queryKey = root.find('QueryKey').text
  count = root.find('Count').text
  retMax = 1000
  retStart = 0

  i = 0
  max = int(count)
  fixed_max = 1000

  print("Total of " + lF + " Abstracts:" + str(max) + ".")
  print("Processing...")

  df = pd.DataFrame(columns=['Title', 'Body', 'Label'])

  while i < max and i < fixed_max:
    
    #Assemble fetch query
    baseFetch = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
    dbF = 'db=pubmed'
    webEnvF = 'WebEnv=' + webEnv
    queryKeyF = 'query_key=' + queryKey
    retStartF = 'retstart=' + str(i)
    retMaxF = 'retmax=' + str(retMax)
    tail = 'retmode=text&rettype=abstract'

    urlFetch = baseFetch + '&' + dbF + '&' + queryKeyF + '&' + webEnvF + '&' + retStartF + '&' + retMaxF + '&' + tail + '&' + email
    

    #Get method
    fetch = requests.get(urlFetch)
    time.sleep(1)

      

    abstracts = re.split('\n\n\n',fetch.text)
    #Assemble Abstracts
    titles = []
    bodies = []

    print("#################   BATCH " + str(i) + "   #################")
    for a in abstracts:
      a_paragraphs = re.split("\n\n", a)
      if len(a_paragraphs) > 4 and "DOI" not in a_paragraphs[4] and len(a_paragraphs[4]) > 100:
        titles.append(a_paragraphs[1])
        bodies.append(a_paragraphs[4])

    labels = [label]*len(titles)
    data = {
      'Title': titles,
      'Body': bodies,
      'Label': labels
    }


    dataSet = pd.DataFrame(data)
    df = pd.concat([df,dataSet])
    print("Count: " + str(df.shape[0]))

    i = i + retMax
    


  return df

df = pd.DataFrame(columns=['Title', 'Body', 'Label'])

species=""

for i in  range(2,len(sys.argv)):
  specie = ntpath.basename(sys.argv[i])
  species += specie
  df2 = getAbstractsfromLabel(specie)
  df = pd.concat([df,df2])

df.to_csv(sys.argv[1] + "/" + species + ".csv",index=False)
