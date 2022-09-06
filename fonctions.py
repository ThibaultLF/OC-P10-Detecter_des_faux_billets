import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import statsmodels
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
import scipy.stats as st
from sklearn.model_selection import train_test_split
from sklearn import decomposition, preprocessing, linear_model
from sklearn.metrics import *
from sklearn.cluster import KMeans
import plotly.figure_factory as ff
import joblib

def var_name(var):
    """Fonction permettant de récupérer le nom de la variable passée en paramètre."""
    for name,value in globals().items() :
        if value is var :
            return name


        
def analyse_primaire(DataFrame):
    """Fonction exécutant les fonctions/propriétés head/dtypes/shape/describe du DataFrame passé en paramètre."""
    nom = var_name(DataFrame)
    fonctions = ['head', 'dtypes', 'shape', 'describe']
    for x in fonctions:
        if callable(object.__getattribute__(DataFrame, x)):
            if x == 'describe':
                print(f"{x}(describe = 'all')")
                display(object.__getattribute__(DataFrame, x)(include = 'all'))
            else:
                print(f"{x}()")
                display(object.__getattribute__(DataFrame, x)())
        else:
            print(f"{x}")
            display(object.__getattribute__(DataFrame, x))



def backward_selected(data, response):
    """Linear model designed by backward selection.

    Parameters:
    -----------
    data : pandas DataFrame with all possible predictors and response

    response: string, name of response column in data

    Returns:
    --------
    model: an "optimal" fitted statsmodels linear model
           with an intercept
           selected by backward selection
           evaluated by parameters p-value
    """
    
    remaining = set(data._get_numeric_data().columns)
    if response in remaining:
        remaining.remove(response)
    cond = True

    while remaining and cond:
        formula = "{} ~ {} + 1".format(response,' + '.join(remaining))
        print('_______________________________')
        print(formula)
        model = smf.ols(formula, data).fit()
        score = model.pvalues[1:]
        toRemove = score[score == score.max()]
        if toRemove.values > 0.05:
            print('remove', toRemove.index[0], '(p-value :', round(toRemove.values[0],3), ')')
            remaining.remove(toRemove.index[0])
        else:
            cond = False
            print('is the final model !')
        print('')
    print(model.summary())
    
    return model


def plot_confusion_matrix(cf_matrix):

    plt.figure(figsize=(7, 7))

    group_names = ['True Neg','False Pos','False Neg','True Pos']

    group_counts = ["{0:0.0f}".format(value) for value in

                    cf_matrix.flatten()]

    group_percentages = ["{0:.2%}".format(value) for value in

                         cf_matrix.flatten()/np.sum(cf_matrix)]

    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in

              zip(group_names,group_counts,group_percentages)]

    labels = np.asarray(labels).reshape(2,2)

    sns.heatmap(cf_matrix, annot=labels, fmt='', cmap='Blues')

 

    plt.title("Prédiction")

    plt.show()
    
def calcul_metric(model, x, y):
    threshold_array = np.linspace(0, 1, 100) # Définition des seuils de classification
    accuracy_list = []
    balanced_accuracy_list = []
    f1_list = []
    f05_list = []

    for threshold in threshold_array:
        # Labels prédits pour un seuil donné
        label_pred_threshold = (model.predict_proba(x)[:,1] > threshold).astype(int)
        
        # Calcul de l'accuracy pour un seuil donné
        accuracy_threshold = accuracy_score(
            y_true=y, y_pred=label_pred_threshold
        )
        accuracy_list.append(accuracy_threshold)
        
        # Calcul de la balanced accuracy pour un seuil donné
        balanced_accuracy_threshold = balanced_accuracy_score(
            y_true=y, y_pred=label_pred_threshold
        )
        balanced_accuracy_list.append(balanced_accuracy_threshold)
        
        # Calcul du f1 pour un seuil donné
        f1_threshold = f1_score(
            y_true=y, y_pred=label_pred_threshold
        )
        f1_list.append(f1_threshold)
        
        # Calcul du f0.5 pour un seuil donné
        f05_threshold = fbeta_score(
            y_true=y, y_pred=label_pred_threshold, beta = 0.5
        )
        f05_list.append(f05_threshold)
        
    return threshold_array, accuracy_list, balanced_accuracy_list, f1_list, f05_list
    
def pred(x):
    if x["is_genuine"] == 1 and x["predict"] == 1:
        return "Vrai positif"
    elif x["is_genuine"] == 1 and x["predict"] == 0:
        return "Faux négatif"
    elif x["is_genuine"] == 0 and x["predict"] == 1:
        return "Faux positif"
    else:
        return "Vrai négatif"
    