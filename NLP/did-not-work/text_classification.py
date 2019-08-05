import glob, random, nltk, similarity_tfidf
from nltk.corpus import movie_reviews
directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/'
text_files = glob.glob(directory + '*.txt')
temp = [open(t).read() for t in text_files]
documents = []
labels = []
master = []
for i in range(0,len(text_files)):
    text = open(text_files[i]).read()
    #print([nltk.word_tokenize(text)])
    documents.append(nltk.word_tokenize(text))
    labels.append(similarity_tfidf.get_single_label(text))

for i in range(0,len(documents)):
    tuple = (documents[i],labels[i])
    master.append(tuple)

random.shuffle(master)

big_document = nltk.word_tokenize(''.join(temp))
#print(big_document[0])

#print(master[0])

# documents = [(list(movie_reviews.words(fileid)), category)
#              for category in movie_reviews.categories()
#              for fileid in movie_reviews.fileids(category)]
# random.shuffle(documents)
# print(documents[1])

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains({})'.format(word)] = (word in document_words)
    return features

all_words = nltk.FreqDist(w.lower() for w in big_document)
word_features = list(all_words)[:1000]
# print(document_features(master[1][0]))
# print(master[1][1])
featuresets = [(document_features(d), c) for (d,c) in master]
#print(len(featuresets))
train_set, test_set = featuresets[400:], featuresets[:86]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)
