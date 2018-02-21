print("Christian")

#Loading libraries and data:

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_boston
boston = load_boston()
print (boston.data.shape)
print (boston.feature_names)
print (np.max(boston.target),np.min(boston.target),np.mean(boston.target))

# Slicing learning set into training and testing datasets:

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test=train_test_split(boston.data,boston.target,test_size=0.25,random_state=33)

#Normalizing the data:

from sklearn.preprocessing import StandardScaler
scalerX=StandardScaler().fit(X_train)
scalery=StandardScaler().fit(y_train)
X_train=scalerX.transform(X_train)
y_train=scalery.transform(y_train)
X_test=scalerX.transform(X_test)
y_test=scalery.transform(y_test)










