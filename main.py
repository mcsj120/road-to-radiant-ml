from re import VERBOSE
import prepareData
import math
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import feature_column


data = prepareData.prepareData()
df = data.normalizedTeamRankSum()

def df_to_dataset(dataframe):
    dataframe = dataframe.copy()
    label1 = dataframe.pop('wpr')
    label2 = dataframe.pop('lpr')
    ds = tf.data.Dataset.from_tensor_slices((dict(dataframe), label1, label2))
    ds = ds.batch(5)
    return ds

train = df[:math.ceil(len(df)*0.8)]
test = df[math.ceil(len(df) * 0.8):]
val = train[:math.ceil(len(train)*0.2)]
train = train[math.ceil(len(train)*0.2):]

train_ds = df_to_dataset(train)
test_ds = df_to_dataset(test)
val_ds = df_to_dataset(val)


feature_columns = []
for header in ['NetSum','sd1','sd2']:
    feature_columns.append(feature_column.numeric_column(header))

feature_layer = tf.keras.layers.DenseFeatures(feature_columns)

model = tf.keras.Sequential([
  feature_layer,
  layers.Dense(9, activation='relu'),
  layers.Dense(9, activation='relu'),
  layers.Dropout(.1),
  layers.Dense(2)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.fit(train_ds,
          #validation_data=val_ds,
          epochs=10)

loss, accuracy = model.evaluate(test_ds, verbose=2)
print("Accuracy", accuracy)
