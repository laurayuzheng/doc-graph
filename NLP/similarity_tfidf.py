#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 13:57:46 2019

@author: laurazheng
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/'
THRESHOLD = 0.2
ML = ['machine learning']
types = ['classification', 'regression']
methods = ['convolutional neural network CNN','support vector SVM','deep neural network DNN',
           'recurrent neural network RNN','temporal neural network TNN','random forest','naive bayes','clustering']
sciences = ['geomorphology','soil','hydrology','meterology','climatology','biogeography',
            'geology','geophysics','ecology','oceanography','limnology','glaciology',
            'meteorology','precipitation','atmospheric']
characteristics = ['heterogeneity','high dimensionality','amorphous boundaries','lack of ground truth','noise']

def get_label(text_files):
    augmented_list = [open(t).read() for t in text_files] + methods
    sims = get_cosine_sim(augmented_list)[:len(text_files), -len(methods):]
    result = []
    result = [np.argmax(t) if max(t)>0 else -1 for t in sims]
    #print(result)
    return result

def get_single_label(text):
    augmented_list = [text] + methods
    sims = get_cosine_sim(augmented_list)[:1, -len(methods):]
    #print(sims)
    result = np.argmax(sims)
    #print(result)
    return methods[result]

def get_relatedness(phrase_list, text_files):
    augmented_list = [open(t).read() for t in text_files] + phrase_list
    sims = get_cosine_sim(augmented_list)[:len(text_files), -len(phrase_list):]
    return sims

def get_cosine_sim(text_files):
    vectors = [t for t in get_vectors(text_files)]
    return cosine_similarity(vectors)

def get_vectors(text_files):
    #text = [t for t in strs]a
    vectorizer = CountVectorizer(text_files)
    vectorizer.fit(text_files)
    return vectorizer.transform(text_files).toarray()


if __name__ == "__main__":
    doc_num = 448
    text_files = glob.glob(directory + '*.txt')
    column_names = ML + sciences + types + characteristics + ['label']
    print(column_names)
    master_matrix = []
    machine_learning_matrix = get_relatedness(ML,text_files)
    types_matrix = get_relatedness(types,text_files)
    sciences_matrix = get_relatedness(sciences, text_files)
    characteristics_matrix = get_relatedness(characteristics, text_files)
    label_array = get_label(text_files)

    for i in range(0,len(types_matrix)):
        #print(np.append(np.append(sciences_matrix[i],types_matrix[i]),characteristics_matrix[i]))
        #print(types_matrix[i])
        #print(characteristics_matrix[i])
        data_row = np.append(machine_learning_matrix[i],sciences_matrix[i])
        data_row = np.append(data_row, types_matrix[i])
        data_row = np.append(data_row, characteristics_matrix[i])
        data_row = np.append(data_row, [label_array[i]])

        #data_row = np.array(np.append(np.append(sciences_matrix[i],types_matrix[i]),characteristics_matrix[i]))
        #data_row = np.append(data_row,[label_array[i]])
        master_matrix.append(data_row)

    #print(master_matrix)
    df = pd.DataFrame(data=master_matrix, columns=column_names)
    #df['index'] = np.arange(len(df))
    rows_drop = df[(df['machine learning'] == 0) | (df['label'] == -1)].index
    df.drop(rows_drop, inplace=True)
    df.to_csv('data.csv', encoding='utf-8', index=False)
    #print(df


    #print("document " + str(doc_num) + ": " + open(text_files[doc_num]).read())

    #print(get_sciences_similarities(text_files))
    #print(get_method_similarities(text_files))
    #print(open(text_files[0]).read())
