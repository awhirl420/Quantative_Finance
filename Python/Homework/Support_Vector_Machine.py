import pandas as pd
import numpy as np
from sklearn import preprocessing, linear_model
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix

pima = pd.read_csv('./dataset/pima-indians-diabetes.csv')

#用'pregnant','insulin','bmi', 'age' 三個變數預測'label'(是否發病)
df=pima[['pregnant', 'insulin', 'bmi', 'age', 'label']]


X=df[['pregnant', 'insulin', 'bmi', 'age']]
y=df['label']

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=1) #random_state 種子值

scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)

model = SVC(kernel='rbf')
model.fit(X_train, y_train) 

X_test = scaler.transform(X_test)
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
num_correct_samples = accuracy_score(y_test, y_pred, normalize=False)

print('number of correct sample: {}'.format(num_correct_samples))
print('accuracy: {}'.format(accuracy))
