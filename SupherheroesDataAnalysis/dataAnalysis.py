import pandas as pd
import plotly.express as px

def preprocessGSMOld(df):
    li = df["GSM"]
    for i in range(len(li)):
        if isinstance(li[i], float):
            li[i] = 0
        elif li[i] == "Homosexual Characters":
            li[i] = 1
        else:
            li[i] = 2
        df["GSM"] = li
        print(df["GSM"])
        return df
    
def preprocessGSM(df):
    return [0 if isinstance(i, float) else 1 if i.startswith("H") else 2 if i.startswith("B") else 3 for i in df]

def preprocessSex(df):
    #NaN is float
    return [0 if isinstance(i, float) else 1 if i.startswith("M") else 2 if i.startswith("F") else 3 if i.startswith("G") else 4 if i.startswith("T") else 5 for i in df]

def preprocessAlign(df):
    return [0 if isinstance(i, float) else 1 if i.startswith("G") else 2 if i.startswith("B") else 3 if i.startswith("N") else 4 if i.startswith("R") else 5 for i in df]

def preprocessID(id):
    return [0 if isinstance(i, float) else 1 if i.startswith("P") else 2 if i.startswith("S") else 3 if i.startswith("U") else 4 for i in id]

def preprocessAlive(df):
    return [0 if isinstance(i, float) else 1 if i.startswith("A") else 2 for i in df]

def preprocessData(df):
    df["GSM"] = preprocessGSM(df["GSM"])
    df["SEX"] = preprocessSex(df["SEX"])
    df["ALIGN"] = preprocessAlign(df["ALIGN"])
    df["ID"] = preprocessID(df["ID"])
    df["ALIVE"] = preprocessAlive(df["ALIVE"])
    return df

def getNumebrOfQueerCharacters(df):
    count = len(list(filter(lambda x: x == 1 or x == 2, df["GSM"])))
    #print("Number of sexual minority members: "+str(count))
    sex = df["SEX"]
    count += len(list(filter(lambda x: x == 3 or x == 4, df["SEX"])))
    return count

def getPercentOfQueerCharactersWihtAlignmentA(df, a):
    num = getNumebrOfQueerCharacters(df)
    alignA = len(list(filter(lambda x: x == a, df["ALIGN"])))
    return alignA / num

def createAlignmentHistorgram(df):
    #queerAlign = list(filter(lambda x: x["GSM"] == 1 or x["GSM"] == 2, df))
    nQueerData = df[(df["GSM"] != 1) & (df["GSM"] != 2)]
    figNormal = px.histogram(nQueerData, x="ALIGN", labels={"values": "total number", "count": "Alignment"})
    figNormal.update_layout(
        xaxis_title ="Alignment (0 = non, 1 = Good, 2 = Bad, 3 = Neutral, 4 = ex Criminal)",
        yaxis_title="Number",
        title = "Non queer character alignment"
    )
    figNormal.show()

    queerData = df[(df["GSM"] == 1) | (df["GSM"] == 2)]
    figQueer = px.histogram(queerData, x="ALIGN", labels={"values": "total number", "count": "Alignment"})
    figQueer.update_layout(
        xaxis_title ="Alignment (0 = non, 1 = Good, 2 = Bad, 3 = Neutral, 4 = ex Criminal)",
        yaxis_title="Number",
        title = "Queer character alignment"
    )
    figQueer.show()

df = pd.read_csv("dc-wikia-data.csv")

preprocessData(df)

print(df)

print("########Report about Queer Representation########")

print("Total number of queer characters: "+str(getNumebrOfQueerCharacters(df)))
print("Percent of Evil queer Characters: "+str(getPercentOfQueerCharactersWihtAlignmentA(df, 2)))
print("Percent of Good queer Characters: "+str(getPercentOfQueerCharactersWihtAlignmentA(df, 1)))

createAlignmentHistorgram(df)
