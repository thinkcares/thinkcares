#Loading libraries and data:

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import sklearn
from sklearn.datasets import load_boston
boston = load_boston()
print (boston.data.shape)
print (boston.target.shape)
print (boston.feature_names)
print (np.max(boston.target),np.min(boston.target),np.mean(boston.target))
bos = pd.DataFrame(boston.data)
bos.columns = boston.feature_names
bos['PRICE'] = boston.target
print(bos.head())
print(bos.describe())
##print(boston.DESCR)

X = bos.drop('PRICE', axis = 1)
Y = bos['PRICE']

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X, Y, test_size = 0.33, random_state = 5)
print(X_train.shape)
print(X_test.shape)
print(Y_train.shape)
print(Y_test.shape)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import SGDRegressor
lm = LinearRegression()
lm.fit(X_train, Y_train)

#pd=lm.predict([[0.38214,   0.0,   6.20,   0.0,  0.5040,  8.040,   86.5,   3.2157,   8.0,  307.0, 17.4,  387.38,   3.13]])
#print (pd)
#print(X_test)
Y_pred = lm.predict(X_test)
print("Predicción: \n",Y_pred)
plt.scatter(Y_test, Y_pred)
plt.xlabel("Prices: $Y_i$")
plt.ylabel("Predicted prices: $\hat{Y}_i$")
plt.title("Prices vs Predicted prices: $Y_i$ vs $\hat{Y}_i$")
plt.show()
mse = sklearn.metrics.mean_squared_error(Y_test, Y_pred)


print ("Coeficientes: \n",lm.coef_)
print("Error cuadrátrico medio:",mse)
print("Coeficiente de correlación R2:", r2_score(Y_test,Y_pred))


#clf=SGDRegressor(loss='squared_loss',penalty=None,random_state=42)
#clf.fit(X_train, Y_train)
#print ("SGDR R2:",clf.score(X_train, Y_train))

#Support Vector Machine (SPV) lineal
from sklearn import svm
clf_svr = svm.SVR(kernel='linear')
clf_svr.fit(X_train, Y_train)
print ("SVR R2:",clf_svr.score(X_train, Y_train))

#clf_svr_poly = svm.SVR(kernel='poly')
#clf_svr_poly.fit(X_train, Y_train)
#print ("SVR POLY R2:",clf_svr_poly.score(X_train, Y_train))

#Support Vector Machine (SPV) RBF (Radial Basis Function)
clf_svr_rbf = svm.SVR(kernel='rbf')
clf_svr_rbf.fit(X_train, Y_train)
print ("RBF R2:",clf_svr_rbf.score(X_train, Y_train))


















