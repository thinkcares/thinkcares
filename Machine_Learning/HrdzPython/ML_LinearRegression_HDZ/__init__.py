import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
import pydotplus
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import cross_val_score, LeaveOneOut
from scipy.stats import sem
from PIL import Image
import matplotlib.pyplot as plt
from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from google.cloud.bigquery import job

# Perform a query.
query = """  
  select   ROW_NUMBER() OVER() KnDia,MfImportePropuesta  
  from (
    SELECT

           year(kdFechaPagoSag) KnYear
            ,DAYOFYEAR(kdFechaPagoSag) KnDayOfYear 
            , sum(MfImportePropuesta)MfImportePropuesta

      FROM
      [stg.tbl_result]
      where dxEstatus='PAGADO'

      group by 
             KnYear
            ,KnDayOfYear  
      ORDER BY 1 ASC ,2 ASC
) tmp1
  
     
  """
# x = pd.read_gbq(query=query,project_id="mx-herdez-analytics",private_key='mx-herdez-analytics-cf83fcf5fcc3.json')
# x.to_csv("DatosHdz.csv")

x = pd.read_csv("DatosHdz.csv")

print("Tamaño del arreglo:",x.shape)
print(x)
print ("Importe máximo:",np.max(x.MfImportePropuesta))
print ("Importe mínimo:", np.min(x.MfImportePropuesta))
print ("Importe promedio:",np.mean(x.MfImportePropuesta))

X = x.drop('MfImportePropuesta', axis = 1)
Y = x['MfImportePropuesta']

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

from sklearn import svm
clf_svr = svm.SVR(kernel='linear')
clf_svr.fit(X_train, Y_train)
print ("SVR R2:",clf_svr.score(X_train, Y_train))

clf_svr_rbf = svm.SVR(kernel='rbf')
clf_svr_rbf.fit(X_train, Y_train)
print ("RBF R2:",clf_svr_rbf.score(X_train, Y_train))