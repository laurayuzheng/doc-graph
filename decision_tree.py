''' Sample decision tree implementation.
Tried to design feature vectors off of similarity to keywords, but it proved to be ineffective.
'''

import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

col_names = ['machine learning', 'geomorphology', 'soil', 'hydrology',
'meterology', 'climatology', 'biogeography', 'geology', 'geophysics', 'ecology',
'oceanography', 'limnology', 'glaciology', 'meteorology', 'precipitation',
'atmospheric', 'classification', 'regression', 'heterogeneity',
'high dimensionality', 'amorphous boundaries', 'lack of ground truth',
'noise', 'label']
# load dataset
data = pd.read_csv("data.csv", header=0, names=col_names)
feature_cols = ['machine learning', 'geomorphology', 'soil', 'hydrology',
'meterology', 'climatology', 'biogeography', 'geology', 'geophysics', 'ecology',
'oceanography', 'limnology', 'glaciology', 'meteorology', 'precipitation',
'atmospheric', 'classification', 'regression', 'heterogeneity',
'high dimensionality', 'amorphous boundaries', 'lack of ground truth',
'noise']
X = data[feature_cols]
y = data.label
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

# Create Decision Tree classifer object
clf = DecisionTreeClassifier()

# Train Decision Tree Classifer
clf = clf.fit(X_train,y_train)

#Predict the response for test dataset
y_pred = clf.predict(X_test)

print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
