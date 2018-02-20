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

df = pd.read_csv('Data/BDArreglada.csv')
df2 = pd.read_csv('Data/Titanic.csv')
feature_names = np.array(df.columns.values)

g =pd.DataFrame( df2.groupby(['sex']).aggregate(np.sum)['survived'])
print(g)

j = g.plot(kind='bar')
plt.ylabel("Sobrevivientes")
plt.title("Sobrevivientes del Titanic")
plt.show()


# print(x)
# j = x.plot(kind='scatter', x='survived', y='sex')
# plt.show()

titanic_X, titanic_y = [], []
titanic_X = np.array(df)
titanic_y = np.array(df["survived"])

# print(feature_names)
# print(titanic_X[0], titanic_y[0])

titanic_X = titanic_X[:, [ 4, 10,11,12,13]]
# los 2 puntos significa TODOS LOS REGISTROS  Y  SOLO OCUPARÁ las columnas 1 pClass, 4 age, 10 sex
feature_names = feature_names[[ 4, 10,11,12,13]]
# solo elige  solo dejar los encabezados de las mismas columnas escogidas
#  tanto en x como en y solo se quedan las columnas  Clase, Edad y Sexo

# print(feature_names)
# print(titanic_X[12], titanic_y[12])

# print(feature_names)
# print(titanic_X[12], titanic_y[12])


print ('New feature names:',feature_names)
# print ('Values:',titanic_X[0])

X_train, X_test, y_train, y_test = train_test_split(titanic_X, titanic_y, test_size=0.25, random_state=33)

clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4,min_samples_leaf=5)
clf = clf.fit(X_train,y_train)

tree.export_graphviz(clf,out_file='titanic.dot', feature_names=feature_names)
graph = pydotplus.graph_from_dot_file('titanic.dot')
graph.write_png('titanic.png')

img1=Image.open('titanic.png')
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
    print("Mean score {0:s}: {1:.3f} (+/-{2:.3f}) \n".format(label,np.mean(scores),sem(scores)))

loo_cv(X_train, y_train, clf,label="Train")
loo_cv(X_test, y_test, clf,label="Test")

""" Ranadom Forest"""
print(">>>>> Random Forest")


from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=10,random_state=33)
clf = clf.fit(X_train,y_train)
loo_cv(X_train,y_train,clf,label="Train")
loo_cv(X_test,y_test,clf,label="Test")


clf_dt=tree.DecisionTreeClassifier(criterion='entropy', max_depth=3,min_samples_leaf=5)
clf_dt.fit(X_train,y_train)
measure_performance(X_test,y_test,clf_dt,label="Test")




def Predice(X, clf):
    y_pred = clf.predict(X)
    print("Valores de Entrada:\n")
    print(X)
    for y in y_pred:
        if y == 1:
            print(">>> Vivio")
        else:
            print(">>> Murio")

# Datos a ingregar para que los prediga el árbol de Decision
valores = pd.DataFrame(
                    [(29,0,1,0,0),
                     (35,1,1,0,0)
                     ]
                     ,columns=feature_names)

Predice(valores,clf)

print("Fin el Pograma de Python, @Bento Sanchez")
