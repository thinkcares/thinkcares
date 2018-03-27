import pandas as pd
import numpy as np
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

SELECT
case when  MfTotalFirmas=3 then 1 else 0 end as Firmas
, case
     when KxEstatusPropuesta ='A' then  1
     else 0
 end as Propuesta
, case
        when KxEstatusPagado in ('K','T') THEN 1
        ELSE 0
 end Pago
, case
       when KxEstatusArch in ('T','R') THEN 1
       else 0
 end Transferido
--, dxestatus
,kbcambiocliente as CambioCliente
, case when KnDifFecFactFecPago=0 then 1 else 0 end PagoEnTiempo
, CASE
       when  MfTotalFirmas<>3 and dxestatus='PAGADO' then 1
       when  (KxEstatusPropuesta='X' OR KxEstatusPagado='X') AND  KxEstatusArch in ('R','T') THEN 1
       when  kbcambiocliente=1 AND  KxEstatusArch in ('R','T') THEN 1
       when  KnDifFecFactFecPago<>0 then 1 
       else 0
end AS Class
FROM stg.tbl_result
where dxestatus in ('PAGADO','REVISAR CANCELADO Y PAGADO')
--AND KXNODOCTO IN ('5645003204','009561320','009649835','009649836','009649837','009649838','009649839','009649840','009649841','009645355','009645810'
--, '009566822','5646237987', '5646385924',
--'009558592','5644550025','5646237987','5646385924'
--) 
  """
df = pd.read_gbq(query=query,project_id="mx-herdez-analytics",private_key='BigQuery/mx-herdez-analytics-cf83fcf5fcc3.json')


# df = pd.read_csv('Data/4_DecesionTree.csv')
# df = pd.read_csv('Data/4_DecesionTreeMas2v2.csv')
feature_names = np.array(df.columns.values)


features_X, labels_y = [], []
features_X = np.array(df)
labels_y = np.array(df["Class"])

print(feature_names)
print(features_X[0], labels_y[0])

features_X = features_X[:, [0,1,2,3,4,5]]
# los 2 puntos significa TODOS LOS REGISTROS  Y  SOLO OCUPARÁ las columnas 1 pClass, 4 age, 10 sex
feature_names = feature_names[[0,1,2,3,4,5]]
# solo elige  solo dejar los encabezados de las mismas columnas escogidas


X_train, X_test, y_train, y_test = train_test_split(features_X, labels_y, test_size=0.25, random_state=33)

clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=3,min_samples_leaf=5)
clf = clf.fit(X_train,y_train)

tree.export_graphviz(clf,out_file='HerdezSet.dot', feature_names=feature_names)
graph = pydotplus.graph_from_dot_file('HerdezSet.dot')
graph.write_png('HerdezSet.png')

img1=Image.open('HerdezSet.png')
plt.imshow(img1)
plt.show()

def measure_performance(X, y, clf ,show_accuracy=True, show_classification_report=True, show_confusion_matrix=True, label=""):
    y_pred = clf.predict(X)
    if show_accuracy:
        print("Accuracy {0:s}: {1:.3f}".format(label, metrics.accuracy_score(y, y_pred)), "\n")
    if show_classification_report:
        print("Classification report")
        print(metrics.classification_report(y, y_pred), "\n")

    if show_confusion_matrix:
        print("Confusion matrix")
        print(metrics.confusion_matrix(y, y_pred), "\n")


measure_performance(X_train, y_train, clf, show_classification_report=False, show_confusion_matrix=False,label="Train")
measure_performance(X_test, y_test, clf ,show_classification_report=False, show_confusion_matrix=False,label="Test")

"""
def loo_cv(X_train,y_train, clf ,label="" ):
    # Perform Leave-One-Out cross validation
    # We are preforming 1313 classifications!
    loo = LeaveOneOut()
    scores = np.zeros(X_train[:].shape[0])
    for train_index, test_index in loo.split(X_train):
        X_train_cv, X_test_cv = X_train[train_index], X_train[test_index]
        y_train_cv, y_test_cv = y_train[train_index], y_train[test_index]
        clf = clf.fit(X_train_cv, y_train_cv)
        y_pred = clf.predict(X_test_cv)
        scores[test_index] = metrics.accuracy_score(y_test_cv.astype(int), y_pred.astype(int))
        # print(">>")
    print("Mean score {0:s}: {1:.3f} (+/-{2:.3f}) \n".format(label,np.mean(scores),sem(scores)))

loo_cv(X_train, y_train, clf,label="Train")
loo_cv(X_test, y_test, clf,label="Test")
"""

""" Ranadom Forest"""
print(">>>>> Random Forest")


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10,random_state=33)
clf = clf.fit(X_train,y_train)
# loo_cv(X_train,y_train,clf,label="Train")
# loo_cv(X_test,y_test,clf,label="Test")


clf_dt=tree.DecisionTreeClassifier(criterion='entropy', max_depth=3,min_samples_leaf=5)
clf_dt.fit(X_train,y_train)
measure_performance(X_test,y_test,clf_dt,label="Test")




def Predice(X, clf):
    y_pred = clf.predict(X)
    print("Valores de Entrada:\n")
    print(X)
    for y in y_pred:
        if y == 1:
            print(">>> Fraude")
        else:
            print(">>> No Fraude")

# Datos a ingregar para que los prediga el árbol de Decision
valores = pd.DataFrame(
                    [
                        (0,    1,    1,    1,    1,    0),
                        (0,    1,    1,    1,    0,    1),
                        (0,    0,    0,    1,    0,    1),
                        (0,    0,    0,    1,    0,    1)
                    ]
                     ,columns=feature_names)

Predice(valores,clf)

print("Fin el Pograma de Python, @Bento Sanchez")


