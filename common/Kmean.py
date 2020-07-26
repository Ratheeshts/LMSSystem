import pandas as pd
import numpy as np
import pandas as pd
import string
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

#load data
xls = pd.ExcelFile('DATA SAMPLES//data.xlsx')
df1 = pd.read_excel(xls, 'learner_static')
df2 = pd.read_excel(xls, 'learning_style')
learner_data=pd.merge(df1,df2,how='inner',on='Sid')
learner_data['Active_Reflective']=''
learner_data['Sensitive_Intutive']=''
learner_data['Visual_Verbal']=''
learner_data['Global_Sequential']=''
columns=list(learner_data.columns) 

#check wether value is dominant
def isDominant(score):
    val=int(score)
    score_min=val-50
    if score_min>0:
        return True
    else:
        return False

def activeOrReflective(score):
    if isDominant(score):
        return 1
    else:
        return 0
    
def sensitiveOrIntutive(score):
    if isDominant(score):
        return '1'
    else:
        return '0'
def visualOrVerbal(score):
    if isDominant(score):
        return '1'
    else:
        return '0'
def Global_Sequential(score):
    if isDominant(score):
        return '1'
    else:
        return '0'
learner_data['Active_Reflective'] = learner_data['Active'].apply(lambda x: activeOrReflective(x))
learner_data['Sensitive_Intutive'] =learner_data['Sensitive'].apply(lambda x: sensitiveOrIntutive(int(x)))
learner_data['Visual_Verbal'] =learner_data.Visual.apply(lambda x: visualOrVerbal(x))
learner_data['Global_Sequential'] =learner_data.Global.apply(lambda x: Global_Sequential(x))
Background=list(learner_data['BackgroundKnowledge'].unique())
Qualification=list(learner_data['Qualification'].unique())

def findBK(bk):
    return Background.index(bk)*100
def findQual(qual):
    return Qualification.index(qual)
learner_data['BackgroundKnowledge'] =learner_data.apply(lambda x: findBK(x['BackgroundKnowledge']), axis=1)
learner_data['Qualification'] =learner_data.apply(lambda x: findQual(x['Qualification']), axis=1)

x_learner_data=learner_data[['BackgroundKnowledge','Active','Sensitive','Visual',]]
ks = range(1, 40)
inertias = []
for k in ks:
    # Create a KMeans instance with k clusters: model
    model = KMeans(n_clusters=k)
    
    # Fit model to samples
    model.fit(x_learner_data)
    
    # Append the inertia to the list of inertias
    inertias.append(model.inertia_)
    
plt.plot(ks, inertias, '-o', color='black')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()
kmeans5 = KMeans(n_clusters=40, random_state=42)
k_predictor= kmeans5.fit(x_learner_data)
x_learner_data['class']=k_predictor.predict(x_learner_data)