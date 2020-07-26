import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from apyori import apriori # you can download this module
import seaborn as sns
%matplotlib inline
data_session_frame=pd.read_excel('sample.xls',sheet_name='LS_Data') #sample excel file
data_session_frame=(data_session_frame.groupby('Session_Id').filter(lambda x: len(x) >= 2))#accept only the sesssion which goes through once02
print('unique Product in dataset = ', len(data_session_frame.VisitedMaterials.unique()))
Uniq_VisitedMaterials= data_session_frame.VisitedMaterials.unique().tolist()  
session_ids=data_session_frame.Session_Id.unique().tolist()
row_array=np.array(len(Uniq_VisitedMaterials))
session_ids
df = pd.DataFrame(columns=Uniq_VisitedMaterials, index=session_ids)
for id in session_ids:
    session_row=data_session_frame.loc[data_session_frame['Session_Id']==id]['VisitedMaterials']
    df.loc[id]['Session_Id']=id
    for m_value in session_row:
         df.loc[id][m_value]=m_value

df.shape
records=[]
for i in range(0,df.shape[0]):
    records.append([str(df.values[i,j]) for j in range(0,df.shape[1])])  
    
association_rules = apriori(records, min_support=0.0045, min_confidence=0.2, min_lift=1, min_length=2)
association_results = list(association_rules)

recommand_df = pd.DataFrame(columns=('Items','Antecedent','Consequent','Support','Confidence','Lift'))
Support =[]
Confidence = []
Lift = []
Items = []
Antecedent = []
Consequent=[]
for RelationRecord in association_results:
    for ordered_stat in RelationRecord.ordered_statistics:
        Support.append(RelationRecord.support)
        Items.append(RelationRecord.items)
        Antecedent.append(ordered_stat.items_base)
        Consequent.append(ordered_stat.items_add)
        Confidence.append(ordered_stat.confidence)
        Lift.append(ordered_stat.lift)
recommand_df['Items'] = list(map(set, Items))                                   
recommand_df['Antecedent'] = list(map(set, Antecedent))
recommand_df['Consequent'] = list(map(set, Consequent))
recommand_df['Support'] = Support
recommand_df['Confidence'] = Confidence
recommand_df['Lift']= Lift