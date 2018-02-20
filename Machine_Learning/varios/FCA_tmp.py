from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from google.cloud.bigquery import job
import matplotlib.pyplot as plt
import numpy as np
import  pandas as pd
import shutil

"""
URL: https://github.com/GoogleCloudPlatform/training-data-analyst/blob/master/CPB100/lab4a/demandforecast.ipynb
Ejemplo : Forecast
"""

client = bigquery.Client.from_service_account_json(json_credentials_path='mx-herdez-analytics-cf83fcf5fcc3.json')
# Perform a query.
query = """
WITH trips AS (
  SELECT EXTRACT (DAYOFYEAR from pickup_datetime) AS daynumber ,
  EXTRACT (DAYOFWEEK from pickup_datetime)  dayofweek
  FROM `bigquery-public-data.new_york.tlc_yellow_trips_*`
  where _TABLE_SUFFIX = @YEAR
)
SELECT daynumber, dayofweek,COUNT(1) AS numtrips FROM trips
GROUP BY daynumber,dayofweek ORDER BY daynumber
"""
query_params = [bigquery.ScalarQueryParameter(name="YEAR",type_="STRING",value='2015')]
job_config = bigquery.QueryJobConfig()
job_config.query_parameters = query_params
query_job = client.query(query, job_config=job_config)
trips  = query_job.result().to_dataframe()
# print(trips)
avg = np.mean(trips['numtrips'])
print('Just using average={0} has RMSE of {1}'.format(avg, np.sqrt(np.mean((trips['numtrips'] - avg)**2))))

wxquery ="""
SELECT EXTRACT (DAYOFYEAR FROM CAST(CONCAT(@YEAR,'-',mo,'-',da) AS TIMESTAMP)) AS daynumber,
       MIN(EXTRACT (DAYOFWEEK FROM CAST(CONCAT(@YEAR,'-',mo,'-',da) AS TIMESTAMP))) dayofweek,
       MIN(min) mintemp, MAX(max) maxtemp, MAX(IF(prcp=99.99,0,prcp)) rain
FROM `bigquery-public-data.noaa_gsod.gsod*`
WHERE stn='725030' AND _TABLE_SUFFIX = @YEAR
GROUP BY 1 ORDER BY daynumber DESC
"""
query_job = client.query(wxquery, job_config=job_config)
weather  = query_job.result().to_dataframe()
# print(weather)
data = pd.merge(weather
                 , trips
                 , on=['daynumber','dayofweek']
                 )

# j = data.plot(kind='scatter', x='maxtemp', y='numtrips')  plt.show()
# j = data.plot(kind='scatter', x='dayofweek', y='numtrips') plt.show()
# j = data[data['dayofweek'] == 7].plot(kind='scatter', x='maxtemp', y='numtrips') plt.show()

print(data.loc[data.daynumber==7])

data2 = data # 2015 data
for year in [2014, 2016]:
    query_parameters = [ bigquery.ScalarQueryParameter(name="YEAR", type_="STRING", value=year)]

    job_config.query_parameters = query_parameters
    query_job = client.query(wxquery, job_config=job_config)
    weather_ = query_job.result().to_dataframe()

    query_job = client.query(query, job_config=job_config)
    trips_ = query_job.result().to_dataframe()
    print(trips_.loc[trips_.daynumber == 7])

    data_for_year = pd.merge(weather_, trips_,  on=['daynumber','dayofweek'])
    data2 = pd.concat([data2, data_for_year])
print(data2.describe())
print(data2.loc[data2.daynumber==7])
print(data2.loc[data2.dayofweek==7])


j = data2[data2['dayofweek'] == 7].plot(kind='scatter', x='maxtemp', y='numtrips')
plt.show()
import tensorflow as tf
shuffled = data2.sample(frac=1, random_state=13)
# It would be a good idea, if we had more data, to treat the days as categorical variables
# with the small amount of data, we have though, the model tends to overfit
print(shuffled.iloc[:,1:5])
predictors = shuffled.iloc[:,1:5]
print(predictors[:5])
print(shuffled[:5])

targets = shuffled.iloc[:,5]
print(targets[:5])

print(len(shuffled['numtrips']))
trainsize = int(len(shuffled['numtrips']) * 0.8)
print(trainsize)
predictors.to_csv('predictors.csv')
shuffled.to_csv('shuffled.csv')
targets.to_csv('targets.csv')
avg = np.mean(shuffled['numtrips'][:trainsize])  # selecciona los primeros registros 876 de dataframe shuffled
rmse = np.sqrt(np.mean((targets[trainsize:] - avg)**2)) # selecciona los últimos registros 876 de dataframe targets
print ('Just using average={0} has RMSE of {1}'.format(avg, rmse))


""" linear regression with tf.contrib.learn """


SCALE_NUM_TRIPS = 600000.0
trainsize = int(len(shuffled['numtrips']) * 0.8)
testsize = len(shuffled['numtrips']) - trainsize
npredictors = len(predictors.columns)
noutputs = 1
tf.logging.set_verbosity(tf.logging.WARN) # change to INFO to get output every 100 steps ...
shutil.rmtree('./trained_model_linear', ignore_errors=True) # so that we don't load weights from previous runs
estimator = tf.contrib.learn.LinearRegressor(model_dir='./trained_model_linear',
                                             feature_columns=tf.contrib.learn.infer_real_valued_columns_from_input(predictors.values))

print ("starting to train ... this will take a while ... use verbosity=INFO to get more verbose output")
def input_fn(features, targets):
  return tf.constant(features.values), tf.constant(targets.values.reshape(len(targets), noutputs)/SCALE_NUM_TRIPS)
estimator.fit(input_fn=lambda: input_fn(predictors[:trainsize], targets[:trainsize]), steps=10000)

pred = np.multiply(list(estimator.predict(predictors[trainsize:].values)), SCALE_NUM_TRIPS )
rmse = np.sqrt(np.mean(np.power((targets[trainsize:].values - pred), 2)))
print ('LinearRegression has RMSE of {0}'.format(rmse))
