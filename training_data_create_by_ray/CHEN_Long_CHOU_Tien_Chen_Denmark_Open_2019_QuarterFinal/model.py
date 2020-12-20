from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
import pandas as pd
import seaborn as sns
import csv
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import learning_curve
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from numpy import mean
from numpy import std
from sklearn.metrics import precision_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import recall_score
import sys
from sklearn.utils import shuffle
from joblib import dump, load


readfile = sys.argv[1]
data = pd.read_csv(readfile)
df = pd.DataFrame(data=data)
df = df.dropna()
#df = shuffle(df)
Y = df.iloc[:,-1]
X = df.iloc[:,2:30]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=466) 

from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


#mnb_nolaplace = DecisionTreeClassifier(criterion='gini',min_samples_leaf=12)
#mnb_nolaplace = make_pipeline(StandardScaler(), SVC(gamma='auto'))
mnb_nolaplace = RandomForestClassifier(n_estimators=100, max_depth=6,oob_score=True)


# load model 
#mnb_nolaplace = load('model.pkl') 
mnb_nolaplace.fit(X_train, y_train)
y_pred = mnb_nolaplace.predict(X_test) 

acc = accuracy_score(y_test, y_pred)
pre = precision_score(y_test, y_pred , average='macro')
cm = confusion_matrix(y_test, y_pred)
recall = recall_score(y_test, y_pred, average='macro')
print(cm)
print('Hold out splitting Accuracy: {:.4f}'.format(acc))
print('Hold out splitting Precision: {:.4f}'.format(pre))
print('Hold out splitting Sensitivity: {:.4f}'.format(recall))
print("\n")
print(classification_report(y_test, y_pred))
dump(mnb_nolaplace,'model1.pkl')
