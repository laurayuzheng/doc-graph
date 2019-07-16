from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import json
import spacy
import numpy

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/'
THRESHOLD = 0.1
methods = ['generative adversarial','naive bayes','random forest',
'support vector', 'linear regression','logistic regression',
'k-means clustering','nearest neighbors','convolutional neural network',
'recurrent neural network']

color_dict = {
    0: 'rgb(229,67,132)',
    1: 'rgb(67,229,132)',
    2: 'rgb(164,67,229)',
    3: 'rgb(229,197,67)',
    4: 'rgb(67,229,229)',
    5: 'rgb(67,100,229)',
    6: 'rgb(229,132,67)',
    7: 'rgb(255,255,255)',
    8: 'rgb(255,51,153)',
    9: 'rgb(76,0,255)'
}

def get_similarities(text_files):
    ''' Description:
        - gets the similarities between each documents

        Parameters:
        - (string) text_files --> a list of paths to each text file

        Returns:
        - triangular matrix of similarities between documents
    '''

    documents = [open(f).read() for f in text_files]
    tfidf = TfidfVectorizer().fit_transform(documents)
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity

def get_method_similarities(text_files):
    ''' Description:
        - gets the similarity between a method and the text

        Parameters:
        - (string) text_files --> list of paths to text file

        Returns:
        - float array that indicates which method (index) is most similar. same size as input
    '''
    nlp = spacy.load('en_core_web_lg')
    documents = [open(f).read() for f in text_files]
    result = []
    for doc in documents:
        similarities = []
        for i in range(0,len(methods)):
            doc_temp = nlp(doc)
            doc2 = nlp(methods[i])
            doc1 = nlp(' '.join([str(t) for t in doc_temp if not t.is_stop]))
            similarities.append(doc1.similarity(doc2))
        #print(similarities)
        result.append(numpy.argmax(similarities))

    return result

# how to construct data? need use a dictionary from pairwise_similarity above
# arguments: m for similarity matrix
def create_json(m, m2, text_files):
    ''' Description:
        - creates json file using python, loads it into a json file for vis.js

        Parameters:
        - m --> (numpy 2d array) matrix of similarities
        - m2 --> (numpy 1d array) array of method classification

        Returns:
        - nothing
    '''
    nodes = []
    edges = []

    m_size = len(m)
    for i in range(0,m_size):
        title = open(text_files[i]).readline().rstrip()
        method = m2[i]
        color = color_dict.get(method,'')
        nodes.append({'id':i, 'label':title, 'color':{'background':color}})

        for j in range(0,i):    # only need until i, since it is triangular
            if m[i][j] >= THRESHOLD:
                edges.append({'from':i, 'to':j})          #, 'weight':m[i][j]})

    data = {'nodes':nodes, 'edges':edges}

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

#if __name__ == '__main__':
#    text_files = glob.glob(directory + '*.txt')
#    similarities = get_similarities(text_files)
    # print(similarities.A)
#    create_json(similarities.A)
#    print('finished!')
