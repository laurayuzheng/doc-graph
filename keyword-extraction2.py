#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:42:11 2019

@author: laurazheng
"""

import pandas as pandas
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import re
import nltk
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
import glob as glob
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from IPython import get_ipython

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/*.txt'
text_files = glob.glob(directory)

def get_dataset():
    documents = {'abstract':[open(f).read() for f in text_files]}
    dataset = pandas.DataFrame(documents)
    dataset['index'] = dataset[['abstract']].index
    dataset['word_count'] = dataset['abstract'].apply(lambda x: len(str(x).split(" ")))
    
    return dataset

lem = WordNetLemmatizer()
stem = PorterStemmer()
stop_words = set(stopwords.words("english"))
new_words = [] #["learning", "data","paper","model","machine","based","method",
             #"result","approach","problem","using","based","used","proposed",
             #"technique","state","application","result","study"]
             
corpus = []
for i in range(0, 71):
    #Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', dataset['abstract'][i])
    
    #Convert to lowercase
    text = text.lower()
    
    #remove tags
    text=re.sub("&lt;/?.*?&gt;"," &lt;&gt; ",text)
    
    # remove special characters and digits
    text=re.sub("(\\d|\\W)+"," ",text)
    
    ##Convert to list from string
    text = text.split()
    
    ##Stemming
    ps=PorterStemmer()
    #Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in  
            stop_words] 
    text = " ".join(text)
    corpus.append(text)
    
print(corpus[70])