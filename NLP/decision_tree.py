import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

label_names = ['convolutional neural network CNN','support vector SVM','deep neural network DNN',
           'recurrent neural network RNN','temporal neural network TNN','random forest','naive bayes','clustering']
col_names = ['machine learning', 'geomorphology', 'soil', 'hydrology', 
             'meterology', 'climatology', 'biogeography', 'geology', 
             'geophysics', 'ecology', 'oceanography', 'limnology', 
             'glaciology', 'meteorology', 'precipitation', 'atmospheric', 
             'classification', 'regression', 'heterogeneity', 
             'high dimensionality', 'amorphous boundaries', 
             'lack of ground truth', 'noise', 'label']
# load dataset
data = pd.read_csv("data.csv", header=0, names=col_names)
#print(data)
feature_cols = ['machine learning', 'geomorphology', 'soil', 'hydrology', 
                'meterology', 'climatology', 'biogeography', 'geology', 
                'geophysics', 'ecology', 'oceanography', 'limnology', 
                'glaciology', 'meteorology', 'precipitation', 'atmospheric', 
                'classification', 'regression', 'heterogeneity', 
                'high dimensionality', 'amorphous boundaries', 
                'lack of ground truth', 'noise']
X = data[feature_cols]
y = data.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# Create Decision Tree classifer object
clf = DecisionTreeClassifier(criterion="entropy", max_depth=7)

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
#y_pred = clf.predict(X_test)

#print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

import graphviz 
from sklearn import tree

dot_data = tree.export_graphviz(clf, out_file='tree.png', 
                     feature_names=feature_cols,  
                     class_names=label_names,  
                     filled=True, rounded=True,  
                     special_characters=True)  
graph = graphviz.Source(dot_data)  
graph.render("iris") 
