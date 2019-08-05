# source: https://www.analyticsvidhya.com/blog/2018/04/a-comprehensive-guide-to-understand-and-implement-text-classification-in-python/

from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

import pandas, xgboost, numpy, textblob, string, similarity_tfidf, glob
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
from xgboost import plot_tree
import matplotlib.pyplot as plt

directory = '/Users/laurazheng/Desktop/NASA Project/doc-graph/extracted_text/*.txt'
text_files = glob.glob(directory)

texts = [open(t).read() for t in text_files]
labels = [similarity_tfidf.get_single_label(open(t).read()) for t in text_files]

#print(texts[0], labels[0])

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = texts
trainDF['label'] = labels

# split the dataset into training and validation datasets
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

#dtrain = xgboost.DMatrix(train_X, label=train_y, feature_names=feature_names)
# label encode the target variable
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)
valid_y = encoder.fit_transform(valid_y)

# create a count vectorizer object
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'])
#print(count_vect)

# create a tokenizer
token = text.Tokenizer()
token.fit_on_texts(trainDF['text'])
word_index = token.word_index

# transform the training and validation data using count vectorizer object
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)
#print(xtrain_count)

# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)

# ngram level tf-idf
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(trainDF['text'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)

# characters level tf-idf
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(trainDF['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x)
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x)

# train a LDA Model
lda_model = decomposition.LatentDirichletAllocation(n_components=20, learning_method='online', max_iter=20)
X_topics = lda_model.fit_transform(xtrain_count)
topic_word = lda_model.components_
vocab = count_vect.get_feature_names()

# view the topic models
n_top_words = 10
topic_summaries = []
for i, topic_dist in enumerate(topic_word):
    topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(n_top_words+1):-1]
    topic_summaries.append(' '.join(topic_words))

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)

    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)

    if is_neural_net:
        predictions = predictions.argmax(axis=-1)

    return metrics.accuracy_score(predictions, valid_y)

# # Naive Bayes on Count Vectors
# accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_count, train_y, xvalid_count)
# print("NB, Count Vectors: ", accuracy)
#
# # Naive Bayes on Word Level TF IDF Vectors
# accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf, train_y, xvalid_tfidf)
# print("NB, WordLevel TF-IDF: ", accuracy)
#
# # Naive Bayes on Ngram Level TF IDF Vectors
# accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
# print("NB, N-Gram Vectors: ", accuracy)
#
# # Naive Bayes on Character Level TF IDF Vectors
# accuracy = train_model(naive_bayes.MultinomialNB(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
# print("NB, CharLevel Vectors: ", accuracy)
#
# # Linear Classifier on Count Vectors
# # best linear classifier so far
# accuracy = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
# print("LR, Count Vectors: ", accuracy)
#
# # Linear Classifier on Word Level TF IDF Vectors
# accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf, train_y, xvalid_tfidf)
# print("LR, WordLevel TF-IDF: ", accuracy)
#
# # Linear Classifier on Ngram Level TF IDF Vectors
# accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
# print("LR, N-Gram Vectors: ", accuracy)
#
# # Linear Classifier on Character Level TF IDF Vectors
# accuracy = train_model(linear_model.LogisticRegression(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
# print("LR, CharLevel Vectors: ", accuracy)
#
# # SVM on Ngram Level TF IDF Vectors
# accuracy = train_model(svm.SVC(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
# print("SVM, N-Gram Vectors: ", accuracy)
#
# # RF on Count Vectors
# accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
# print("RF, Count Vectors: ", accuracy)
#
# # RF on Word Level TF IDF Vectors
# accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf, train_y, xvalid_tfidf)
# print("RF, WordLevel TF-IDF: ", accuracy)


# Xgb, Count Vectors:  0.8524590163934426
# Xgb, WordLevel TF-IDF:  0.8524590163934426
# Xgb, CharLevel Vectors:  0.7540983606557377
# Extereme Gradient Boosting on Count Vectors
model = xgboost.XGBClassifier()
accuracy = train_model(model, xtrain_count.tocsc(), train_y, xvalid_count.tocsc())
print("Xgb, Count Vectors: ", accuracy)

# Extereme Gradient Boosting on Word Level TF IDF Vectors
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y, xvalid_tfidf.tocsc())
print("Xgb, WordLevel TF-IDF: ", accuracy)

# Extereme Gradient Boosting on Character Level TF IDF Vectors
accuracy = train_model(xgboost.XGBClassifier(), xtrain_tfidf_ngram_chars.tocsc(), train_y, xvalid_tfidf_ngram_chars.tocsc())
print("Xgb, CharLevel Vectors: ", accuracy)

plot_tree(model)
plt.show()

model.save_model('xgbooster.model')
#Save the model to a file.

#The model is saved in an XGBoost internal binary format which is universal among the various XGBoost interfaces. Auxiliary attributes of the Python Booster object (such as feature names) will not be loaded. Label encodings (text labels to numeric labels) will be also lost. If you are using only the Python interface, we recommend pickling the model object for best results.

#Parameters
#fname (string) – Output file name
# def create_model_architecture(input_size):
#     # create input layer
#     input_layer = layers.Input((input_size, ), sparse=True)
#
#     # create hidden layer
#     hidden_layer = layers.Dense(100, activation="relu")(input_layer)
#
#     # create output layer
#     output_layer = layers.Dense(1, activation="sigmoid")(hidden_layer)
#
#     classifier = models.Model(inputs = input_layer, outputs = output_layer)
#     classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
#     return classifier
#
# classifier = create_model_architecture(xtrain_tfidf_ngram.shape[1])
# accuracy = train_model(classifier, xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram, is_neural_net=True)
# print("NN, Ngram Level TF IDF Vectors",  accuracy)
#
# def create_cnn():
#     # Add an Input Layer
#     input_layer = layers.Input((70,))
#
#     # Add the word embedding Layer
#     embedding_layer = layers.Embedding(len(word_index) + 1, 300, weights=[embedding_matrix], trainable=False)(input_layer)
#     embedding_layer = layers.SpatialDropout1D(0.3)(embedding_layer)
#
#     # Add the convolutional Layer
#     conv_layer = layers.Convolution1D(100, 3, activation="relu")(embedding_layer)
#
#     # Add the pooling Layer
#     pooling_layer = layers.GlobalMaxPool1D()(conv_layer)
#
#     # Add the output Layers
#     output_layer1 = layers.Dense(50, activation="relu")(pooling_layer)
#     output_layer1 = layers.Dropout(0.25)(output_layer1)
#     output_layer2 = layers.Dense(1, activation="sigmoid")(output_layer1)
#
#     # Compile the model
#     model = models.Model(inputs=input_layer, outputs=output_layer2)
#     model.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
#
#     return model
#
# classifier = create_cnn()
# accuracy = train_model(classifier, train_seq_x, train_y, valid_seq_x, is_neural_net=True)
# print("CNN, Word Embeddings",  accuracy)
