import pandas as pd
import numpy as np
import copy

query = """  
SELECT * FROM stg.data_4_cluster_20180130 
  """
df = pd.read_gbq(query=query,project_id="mx-herdez-analytics",private_key='BigQuery/mx-herdez-analytics-cf83fcf5fcc3.json')

dic_df={}
dic_df_random={}
# print(df)

dias={1,2,3,4,5,6,7,8}

for dia in dias:
    key_name = 'df' + str(dia)
    rowsCount = len(df[df["KnDayOfWeek"] == dia])
    if rowsCount>0:
        dic_df[key_name]=pd.DataFrame(df[df["KnDayOfWeek"]==dia])
        print(len(dic_df[key_name]))
        dic_df_random[key_name] = pd.DataFrame.sample(pd.DataFrame(df[df["KnDayOfWeek"]==dia]), frac=.10, random_state=33)
        print(len(dic_df_random[key_name]))


print("salir")

