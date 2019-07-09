from sklearn.feature_extraction.text import TfidfVectorizer
import glob
import json

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/'

def get_similarities(text_files):
    ''' Description:
        - gets the similarities between each documents

        Parameters:
        - text_files is a string list of paths to each text file

        Returns:
        - triangular matrix of similarities between documents
    '''

    documents = [open(f).read() for f in text_files]
    tfidf = TfidfVectorizer().fit_transform(documents)
    # no need to normalize, since Vectorizer will return normalized tf-idf
    pairwise_similarity = tfidf * tfidf.T
    return pairwise_similarity

# how to construct data? need use a dictionary from pairwise_similarity above
# arguments: m for similarity matrix
def create_json(m):
    ''' Description:
        - creates json file using python, loads it into a json file for vis.js

        Parameters:
        - m --> matrix of similarities

        Returns:
        - nothing
    '''

    nodes = []
    edges = []

    m_size = len(m)
    for i in range(0,m_size):
        title = open(text_files[i]).readline().rstrip()
        nodes.append({'id':i, 'label':title})

        for j in range(0,i):    # only need until i, since it is triangular
            if m[i][j] >= 0.2:
                edges.append({'from':i, 'to':j})          #, 'weight':m[i][j]})

    data = {'nodes':nodes, 'edges':edges}

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    text_files = glob.glob(directory + '*.txt')
    similarities = get_similarities(text_files)
    #print(similarities.A)
    create_json(similarities.A)
