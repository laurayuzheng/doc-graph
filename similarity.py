#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:57:46 2019

@author: laurazheng
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import spacy
import numpy

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/'
THRESHOLD = 0.2
types = ['classification', 'regression']
methods = ['convolutional neural network CNN','support vector SVM','deep neural network DNN',
           'recurrent neural network RNN','temporal neural network TNN','random forest']
sciences = ['geomorphology','soil','hydrology','meterology','climatology','biogeography',
            'geology','geophysics','ecology','oceanography','limnology','glaciology',
            'meteorology','precipitation','atmospheric']

#def get_method_similarities(text_files):
#    ''' Description:
#        - gets the similarity between a method and the text
#
#        Parameters:
#        - (string) text_files --> list of paths to text file
#
#        Returns:
#        - float array that indicates which method (index) is most similar. same size as input
#    '''
#    nlp = spacy.load('en_core_web_lg')
#    documents = [open(f).read() for f in text_files]
#    result = []
#    for doc in documents:
#        similarities = []
#        for i in range(0,len(methods)):
#            doc_temp = nlp(doc)
#            doc2 = nlp(methods[i])
#            doc1 = nlp(' '.join([str(t) for t in doc_temp if not t.is_stop]))
#            similarities.append(doc1.similarity(doc2))
#        #print(similarities)
#        result.append(methods[numpy.argmax(similarities)])
#
#    return result
#
#def get_sciences_similarities(text_files):
#    ''' Description:
#        - gets the similarity between a science and the text
#
#        Parameters:
#        - (string) text_files --> list of paths to text file
#
#        Returns:
#        - float array that indicates which method (index) is most similar. same size as input
#    '''
#    nlp = spacy.load('en_core_web_lg')
#    documents = [open(f).read() for f in text_files]
#    result = []
#    for doc in documents:
#        similarities = []
#        for i in range(0,len(sciences)):
#            doc_temp = nlp(doc)
#            doc2 = nlp(sciences[i])
#            doc2 = nlp('deep neural network')
#            doc3 = nlp('temporal neural network')
#            doc1 = nlp(' '.join([str(t) for t in doc_temp if not t.is_stop]))
#            print(doc1)
#            print(doc2)
#            print(doc1.similarity(doc2))
#            print(doc1.similarity(doc3))
#            return
#            similarities.append(doc1.similarity(doc2))
#        #print(similarities)
#        result.append(sciences[numpy.argmax(similarities)])
#
#    return result

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def get_cosine_sim(text_files): 
    vectors = [t for t in get_vectors(text_files)]
    return cosine_similarity(vectors)
    
def get_vectors(text_files):
    #text = [t for t in strs]
    vectorizer = CountVectorizer(text_files)
    vectorizer.fit(text_files)
    return vectorizer.transform(text_files).toarray()

def get_sciences_similarities(text_files):
    sciences2 = [open(t).read() for t in text_files] + sciences
    science_sim = get_cosine_sim(sciences2)[:len(text_files), -len(sciences):]
    return science_sim

if __name__ == "__main__":
    doc_num = 33
    text_files = glob.glob(directory + '*.txt')
    doc_sciences = get_sciences_similarities(text_files)
    for i in range(0,len(doc_sciences)):
        print("document " + str(i) + ": ")
        if max(doc_sciences[i]) != 0:
            print(sciences[numpy.argmax(doc_sciences[i])])
        else:
            print("no earth science detectable")
        print()
    print("document " + str(doc_num) + ": " + open(text_files[doc_num]).read())
    
    #print(get_sciences_similarities(text_files))
    #print(get_method_similarities(text_files))
    #print(open(text_files[0]).read())