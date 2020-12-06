import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing


# load csv file
df = pd.read_csv('./housing.csv', header=None, delim_whitespace=True)
print(df.head())

# separate features and label
y = df[13]
X = df.drop([13], axis=1)
# split data into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1)

# normalize data
scaler = preprocessing.StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)

# build model 
model = linear_model.LinearRegression()
model.fit(X_train, y_train)

# evaluate result 
X_test = scaler.transform(X_test)
y_pred = model.predict(X_test)

# The coefficients
print('Coefficients: {}\n'.format(model.coef_))
# The mean squared error
print("Mean squared error: {}".format(mean_squared_error(y_test, y_pred)))
# Explained variance score: 1 is perfect prediction
print('R2 score: {}'.format(r2_score(y_test, y_pred)))
