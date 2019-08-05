import glob
import pandas as pd
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from gensim import corpora, models

from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np
#np.random.seed(2018)

import nltk
#nltk.download('wordnet')

from pprint import pprint

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/*.txt'

def lemmatize_stemming(text):
    return SnowballStemmer('english').stem(WordNetLemmatizer().lemmatize(text, pos='v'))

def preprocess_single(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result

def preprocess(text_files):
    documents = {'abstract':[open(f).read() for f in text_files]}
    data = pd.DataFrame(documents)
    data['index'] = data[['abstract']].index
    processed_docs = data['abstract'].map(preprocess_single)

    #doc_sample = data[data['index'] == 5].values[0][0]
    #print('original document: ')
    #words = []
    #for word in doc_sample.split(' '):
    #    words.append(word)
    #print(words)
    #print('\n\n tokenized and lemmatized document: ')
    #print(preprocess_single(doc_sample))

    return processed_docs

def bag_of_words(processed_docs):
    dictionary = gensim.corpora.Dictionary(processed_docs)

    #count = 0
    #for k, v in dictionary.iteritems():
    #    print(k, v)
    #    count += 1
    #    if count > 10:
    #        break
    dictionary.filter_extremes(no_below=0.1, no_above=2, keep_n=100000)
    bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]

    #bow_doc_0 = bow_corpus[0]
    #print_bow_doc(dictionary,bow_doc_0)

    tfidf = models.TfidfModel(bow_corpus)
    #print(tfidf)
    corpus_tfidf = tfidf[bow_corpus]
    # for doc in corpus_tfidf:
    #    pprint(doc)
    #    break

    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=3,
                                id2word=dictionary, passes=200, workers=3)
    for idx, topic in lda_model.print_topics(-1):
        print('Topic: {} \nWords: {}'.format(idx, topic))


def print_bow_doc(dictionary,bow_doc):
    for i in range(len(bow_doc)):
        print("Word {} (\"{}\") appears {} time.".format(bow_doc[i][0],
                                                   dictionary[bow_doc[i][0]],
                                                   bow_doc[i][1]))

if __name__ == "__main__":
    text_files = glob.glob(directory)
    print(text_files[4:5])
    docs = preprocess(text_files[4:5])
    #print(docs)
    bag_of_words(docs)
