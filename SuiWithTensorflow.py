import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import sklearn
import sklearn.model_selection

df = pd.read_csv("master.csv")
print(df.columns)
countrys = {}
i = 0
for s in df["country"]:
    if not s in countrys:
        countrys[s] = i
        i+=1
print(countrys)
for i in range(len(df)):
    df["country"][i] = countrys[df["country"][i]]
print(df)
for i in range(len(df)):
    if df["sex"][i] == "male":
        df["sex"][i] = 1
    else:
        df["sex"][i] = 0
print(df)

generation = {}
i = 0
for s in df["generation"]:
    if not s in generation:
        generation[s] = i
        i+=1
print(generation)

for i in range(len(df)):
    df["generation"][i] = generation[df["generation"][i]]
print(df)

age = {}
i = 0
for s in df["age"]:
    if not s in age:
        age[s] = i
        i+=1
print(age)

for i in range(len(df)):
    if(df["age"][i] == "5-14 years"):
        df["age"][i] = 0
    elif(df["age"][i] == "15-24 years"):
        df["age"][i] = 1
    elif(df["age"][i] == "25-34 years"):
        df["age"][i] = 2
    elif(df["age"][i] == "35-54 years"):
        df["age"][i] = 3
    elif(df["age"][i] == "55-74 years"):
        df["age"][i] = 4
    elif(df["age"][i] == "75+ years"):
        df["age"][i] = 5
print("Done")
print(df)
df = df.drop("country-year", axis = 1)
print(df)
#remove the commatas from gdp_for_year ($)
for i in range(len(df)):
    df[" gdp_for_year ($) "][i] = int(df[" gdp_for_year ($) "][i].replace(",", ""))
print(df)
m = max(df[" gdp_for_year ($) "])
for i in range(len(df)):
    df[" gdp_for_year ($) "][i] /= m
print(df)
for s in df.columns:
    m = max(df[s])
    for i in range(len(df)):
        df[s][i] /= m
print(df)
print(df.columns)
"""y = []
for i in range(len(df)):
    y.append(df["suicides_no"][i])
print(y)"""
y = df.suicides_no
print(y)
X = df.drop("suicides_no", axis = 1)
X = X.drop("suicides/100k pop", axis = 1)
X = np.asarray(X).astype("float32")
y = np.asarray(X).astype("float32")
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size = 100) 
model = keras.Sequential([
    keras.layers.Dense(11, activation = "relu"),
    keras.layers.Dense(6, activation = "relu"),
    keras.layers.Dense(1, activation = "linear")
    ])
model.compile(optimizer = "adam", loss = "mean_squared_error", metrics=["accuracy"])
model.fit(x_train, y_train, epochs = 200)
