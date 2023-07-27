import pandas as pd
import numpy as np
import random


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


data = pd.read_csv("train.csv")
Y = data["Survived"]
X = data.drop("Survived", axis=1)
X = convertGender(X)
X = convertEmbarked(X)
X = dropUselessColumns(X)
X = insertMissingAge(X)
X = normalizeValues(X)

