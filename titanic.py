import pandas as pd
import random
import tensorflow as tf
from sklearn.model_selection import train_test_split


def convertGender(X):
    X["Sex"] = X["Sex"].map({"male": 0, "female": 1})
    return X


def convertEmbarked(X):
    X["Embarked"] = X["Embarked"].map({"C": 0, "Q": 1, "S": 2})
    X["Embarked"].fillna(random.randint(0, 2), inplace = True)
    return X


def dropUselessColumns(X):
    X = X.drop("Name", axis = 1)
    X = X.drop("Ticket", axis = 1)
    X = X.drop("Cabin", axis = 1)
    X = X.drop("PassengerId", axis = 1)
    return X


def insertMissingAge(X):
    medianAge = X["Age"][round(len(X)/2)]
    X["Age"].fillna(medianAge, inplace = True)
    return X


def normalizeValues(X):
    for c in X.columns.tolist():
        X[c] = (X[c] - X[c].min()) / (X[c].max() - X[c].min())
    return X


def createX(X):    
    X = data.drop("Survived", axis=1)
    X = convertGender(X)
    X = convertEmbarked(X)
    X = dropUselessColumns(X)
    X = insertMissingAge(X)
    X = normalizeValues(X)
    return X


data = pd.read_csv("train.csv")
Y = data["Survived"]
X = createX(data)
X, X_test, Y, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 42)
"""
# simple model with adam
Loss: 0.4865436553955078
Accuracy 0.8156424760818481

model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "sigmoid")
])

loss = "binary_crossentropy"
optimizer = "adam"

model.compile(loss = loss, optimizer = optimizer, metrics = ["accuracy"])
"""

"""
# tanh
Loss: 0.7248475551605225
Accuracy 0.8100558519363403
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "tanh")
])

loss = "binary_crossentropy"
optimizer = "adam"
"""
"""
Loss: 0.42288151383399963
Accuracy 0.8044692873954773

# simple model fixed learning rate
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "sigmoid")
])

loss = "binary_crossentropy"
learning_rate = 0.01
optimizer = tf.keras.optimizers.SGD(learning_rate=learning_rate)
"""

"""
# extra relu layer

Loss: 0.7285986542701721
Accuracy 0.8100558519363403

model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(8, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "sigmoid")
])

loss = "binary_crossentropy"
optimizer = "adam"
"""
"""
# deeper Model with morde neurons
Loss: 1.7817386388778687
Accuracy 0.7541899681091309
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(64, activation = "relu"),
    tf.keras.layers.Dense(32, activation = "relu"),
    tf.keras.layers.Dense(16, activation = "relu"),
    tf.keras.layers.Dense(8, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "sigmoid")
])

loss = "binary_crossentropy"
optimizer = "adam"
"""

"""

Loss: 0.8786811828613281
Accuracy 0.8156424760818481
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation = "relu", input_dim = len(X.columns)),
    tf.keras.layers.Dense(64, activation = "relu"),
    tf.keras.layers.Dense(1, activation = "sigmoid")
])

loss = "binary_crossentropy"
optimizer = "adam"
"""

model.compile(loss = loss, optimizer = optimizer, metrics = ["accuracy"])
model.fit(X, Y, epochs = 1000, batch_size = 32, validation_split = 0.1)

loss, accuracy = model.evaluate(X_test, Y_test)
print("Loss: "+str(loss))
print("Accuracy "+str(accuracy))
