import os
import gc
import json
#import visual_genome as vg
#import visual_genome.local as local
#from visual_genome.models import (Image, Object, Attribute, Relationship, Graph, Synset)
import requests
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import bulk
from elasticsearch_dsl.query import Bool, MultiMatch
from elasticsearch_dsl.search import Search, MultiSearch
from elasticsearch_dsl import Mapping, Keyword, Nested, Text
from elasticsearch_dsl import Index, analyzer, tokenizer
from elasticsearch_dsl import Q
import glob
#import cv2
#import numpy as np
#from matplotlib import pyplot as plt

res = requests.get('http://localhost:9200')
print (res.content)
es = Elasticsearch([{'host': 'localhost', 'port': '9200'}])
client = Elasticsearch()

id = Index('idxi20') #  
id.delete(using=client)

id = Index('idxo20') # 
id.delete(using=client)

