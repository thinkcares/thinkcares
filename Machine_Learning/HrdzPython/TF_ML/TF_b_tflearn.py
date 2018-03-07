from google.cloud import bigquery
from google.cloud.bigquery import Dataset
from google.cloud.bigquery import job
import tensorflow as tf
from tensorflow.contrib import layers
import pandas as pd
import pandas_gbq as pd_gbq
import numpy as np
import shutil
import itertools

print(tf.__version__)

# in CSV, target is the first column, after the features, followed by the key
CSV_COLUMNS = ['fare_amount', 'pickuplon','pickuplat','dropofflon','dropofflat','passengers', 'key']
FEATURES = CSV_COLUMNS[1:len(CSV_COLUMNS)-1]
TARGET = CSV_COLUMNS[0]

df_train = pd.read_csv('./taxi-train.csv', header=None, names=CSV_COLUMNS)
df_valid = pd.read_csv('./taxi-valid.csv', header=None, names=CSV_COLUMNS)


def make_input_fn(df):
    def pandas_to_tf(pdcol):
        # convert the pandas column values to float
        t = tf.constant(pdcol.astype('float32').values)
        # take the column which is of shape (N) and make it (N, 1)
        return tf.expand_dims(t, -1)

    def input_fn():
        # create features, columns
        features = {k: pandas_to_tf(df[k]) for k in FEATURES}
        labels = tf.constant(df[TARGET].values)
        return features, labels

    return input_fn


def make_feature_cols():
    input_columns = [tf.contrib.layers.real_valued_column(k) for k in FEATURES]
    return input_columns

tf.logging.set_verbosity(tf.logging.INFO)
shutil.rmtree('taxi_trained', ignore_errors=True) # start fresh each time
model = tf.contrib.learn.LinearRegressor(
      feature_columns=make_feature_cols(), model_dir='taxi_trained')
model.fit(input_fn=make_input_fn(df_train), steps=10);


def print_rmse(model, name, input_fn):
  metrics = model.evaluate(input_fn=input_fn, steps=1)
  print('RMSE on {} dataset = {}'.format(name, np.sqrt(metrics['loss'])))
print_rmse(model, 'validation', make_input_fn(df_valid))

print(">>>>>Regresión Lineal")
# read saved model and use it for prediction
model = tf.contrib.learn.LinearRegressor(feature_columns=make_feature_cols(), model_dir='taxi_trained')
preds_iter = model.predict(input_fn=make_input_fn(df_valid))
print(list(itertools.islice(preds_iter, 5))) # first 5

print(">>>>>Deep Neuronal Network")

tf.logging.set_verbosity(tf.logging.INFO)
shutil.rmtree('taxi_trained', ignore_errors=True) # start fresh each time
model = tf.contrib.learn.DNNRegressor(hidden_units=[32, 8, 2],
      feature_columns=make_feature_cols(), model_dir='taxi_trained')
model.fit(input_fn=make_input_fn(df_train), steps=100);
print_rmse(model, 'validation', make_input_fn(df_valid))



def create_query(phase, EVERY_N):
        """
        phase: 1=train 2=valid
        """
        base_query = """
        SELECT
      (tolls_amount + fare_amount) AS fare_amount,
      CONCAT(STRING(pickup_datetime), STRING(pickup_longitude), STRING(pickup_latitude), STRING(dropoff_latitude), STRING(dropoff_longitude)) AS key,
      DAYOFWEEK(pickup_datetime)*1.0 AS dayofweek,
      HOUR(pickup_datetime)*1.0 AS hourofday,
      pickup_longitude AS pickuplon,
      pickup_latitude AS pickuplat,
      dropoff_longitude AS dropofflon,
      dropoff_latitude AS dropofflat,
      passenger_count*1.0 AS passengers
    FROM
       [nyc-tlc:yellow.trips]
    WHERE
      trip_distance > 0
      AND fare_amount >= 2.5
      AND pickup_longitude > -78
      AND pickup_longitude < -70
      AND dropoff_longitude > -78
      AND dropoff_longitude < -70
      AND pickup_latitude > 37
      AND pickup_latitude < 45
      AND dropoff_latitude > 37
      AND dropoff_latitude < 45
      AND passenger_count > 0
      """

        if EVERY_N == None:
            if phase < 2:
                # training
                query = "{0} AND ABS(HASH(pickup_datetime)) % 4 < 2".format(base_query)
            else:
                query = "{0} AND ABS(HASH(pickup_datetime)) % 4 == {1}".format(base_query, phase)
        else:
            query = "{0} AND ABS(HASH(pickup_datetime)) % {1} == {2}".format(base_query, EVERY_N, phase)

        return query


query = create_query(2, 100000)
# print(query)
client = bigquery.Client.from_service_account_json(json_credentials_path='mx-herdez-analytics-cf83fcf5fcc3.json')

query_job = client.query(query)
job_config = bigquery.QueryJobConfig()

# Set use_legacy_sql to False to use standard SQL syntax.
# Note that queries are treated as standard SQL by default.
job_config.use_legacy_sql = True
query_job = client.query(query, job_config=job_config)
df = query_job.result().to_dataframe()
print_rmse(model, 'benchmark', make_input_fn(df))



# ejercicio C
print("inicia ejercicio c")

CSV_COLUMNS = ['fare_amount', 'pickuplon','pickuplat','dropofflon','dropofflat','passengers', 'key']
LABEL_COLUMN = 'fare_amount'
DEFAULTS = [[0.0], [-74.0], [40.0], [-74.0], [40.7], [1.0], ['nokey']]


def read_dataset(filename, num_epochs=None, batch_size=512, mode=tf.contrib.learn.ModeKeys.TRAIN):
    def _input_fn():
        input_file_names = tf.train.match_filenames_once(filename)
        filename_queue = tf.train.string_input_producer(input_file_names, num_epochs=num_epochs, shuffle=True)
        reader = tf.TextLineReader()
        _, value = reader.read_up_to(filename_queue, num_records=batch_size)
        value_column = tf.expand_dims(value, -1)
        columns = tf.decode_csv(value_column, record_defaults=DEFAULTS)
        features = dict(zip(CSV_COLUMNS, columns))
        label = features.pop(LABEL_COLUMN)
        return features, label
    return _input_fn


def get_train():
    return read_dataset('taxi-train.csv', num_epochs=100, mode=tf.contrib.learn.ModeKeys.TRAIN)


def get_valid():
    return read_dataset('taxi-valid.csv', num_epochs=1, mode=tf.contrib.learn.ModeKeys.EVAL)


def get_test():
    return read_dataset('taxi-test.csv', num_epochs=1, mode=tf.contrib.learn.ModeKeys.EVAL)


INPUT_COLUMNS = [
    layers.real_valued_column('pickuplon'),
    layers.real_valued_column('pickuplat'),
    layers.real_valued_column('dropofflat'),
    layers.real_valued_column('dropofflon'),
    layers.real_valued_column('passengers'),
]

feature_cols = INPUT_COLUMNS
tf.logging.set_verbosity(tf.logging.INFO)
shutil.rmtree('taxi_trained', ignore_errors=True) # start fresh each time
model = tf.contrib.learn.LinearRegressor(feature_columns=feature_cols, model_dir='taxi_trained')
model.fit(input_fn=get_train());


def print_rmse(model, name, input_fn):
  metrics = model.evaluate(input_fn=input_fn, steps=1)
  print('RMSE on {} dataset = {}'.format(name, np.sqrt(metrics['loss'])))


print_rmse(model, 'validation', get_valid())
print_rmse(model, 'test', get_test())
print_rmse(model, 'train', get_train())