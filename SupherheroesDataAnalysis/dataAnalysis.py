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
    return [0 if isinstance(x, float) else 1 if x.startswith("H") else 2 if x.startswith("B") else 3 for x in df["GSM"]]
    return df["GSM"].apply(lambda x: 0 if isinstance(x, float) else 1 if x.startswith("H") else 2 if x.startswith("B") else 3)


def preprocessSex(df):
    #NaN is float
    return df["SEX"].apply(lambda x: 0 if isinstance(x, float) else 1 if x.startswith("M") else 2 if x.startswith("F") else 3 if x.startswith("G") else 4 if x.startswith("T") else 5)


def preprocessAlign(df):
    return df["ALIGN"].apply(lambda x: 0 if isinstance(x, float) else 1 if x.startswith("G") else 2 if x.startswith("B") else 3 if x.startswith("N") else 4 if x.startswith("R") else 5)


def preprocessID(id):
     return df["ID"].apply(lambda x: 0 if isinstance(x, float) else 1 if x.startswith("P") else 2 if x.startswith("S") else 3 if x.startswith("U") else 4)


def preprocessAlive(df):
    return df["ALIVE"].apply(lambda x: 0 if isinstance(x, float) else 1 if x.startswith("L") else 2)


def preprocessData(df):
    df["GSM"] = preprocessGSM(df)
    df["SEX"] = preprocessSex(df)
    df["ALIGN"] = preprocessAlign(df)
    df["ID"] = preprocessID(df)
    df["ALIVE"] = preprocessAlive(df)
    return df


def getNumebrOfQueerCharacters(df):
    count = len(list(filter(lambda x: x == 1 or x == 2, df["GSM"])))
    count += len(list(filter(lambda x: x == 3 or x == 4, df["SEX"])))
    return count


def isQueer(el):
    if el["GSM"] == 1 or el["GSM"] == 2:
        return True
    if el["SEX"] == 3 or el["SEX"] == 4:
        return True
    return False
    

def getPercentOfCharactersWithAlignment(df, a):
    alignA = df[df["ALIGN"] == a]
    alignA = alignA[(alignA["GSM"] != 1) & (alignA["GSM"] != 2) & (alignA["SEX"] != 3) & (alignA["SEX"] != 4)]
    # 
    return len(alignA) / len(df)


def getPercentOfQueerCharactersWithAlignmentA(df, a):
    alignA = df[df["ALIGN"] == a]
    alignA = alignA[(alignA["GSM"] == 1) | (alignA["GSM"] == 2) | (alignA["SEX"] == 3) | (alignA["SEX"] == 4)]
    return len(alignA) / getNumebrOfQueerCharacters(df)


def getDeathProbablityOfNotQueerCharacters(df):
    aliveList = df[df["ALIVE"] == 1]
    print(len(aliveList))
    aliveList = aliveList[(aliveList["GSM"] != 1) & (aliveList["GSM"] != 2) & (aliveList["SEX"] != 3) & (aliveList["SEX"] != 4)]
    print(len(aliveList))
    return len(aliveList) / len(df)


def getDeathProbabilityForQueerCharacters(df):
    aliveList = df[df["ALIVE"] == 1]
    aliveList = aliveList[(aliveList["GSM"] == 1) | (aliveList["GSM"] == 2) | (aliveList["SEX"] == 3) | (aliveList["SEX"] == 4)]
    return len(aliveList) / getNumebrOfQueerCharacters(df)


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

df = preprocessData(df)

print(df["SEX"])

#createAlignmentHistorgram(df)

print("########Report about Queer Representation########")

print("Total number of queer characters: "+str(getNumebrOfQueerCharacters(df)))
print("Percent of evil characters: " + str(getPercentOfCharactersWithAlignment(df, 2)))
print("Percent of Evil queer Characters: "+str(round(getPercentOfQueerCharactersWithAlignmentA(df, 2), 3)*100)+"%")
print("VS the percent of non queer evil characters: ")
print("Percent of Good queer Characters: "+str(round(getPercentOfQueerCharactersWithAlignmentA(df, 1), 2)*100)+"%")


print("Probability for a queer Character to stay alive: "+str(round(getDeathProbabilityForQueerCharacters(df), 2)*100)+"%")
print("Probability for a non queer Character to stay alive: "+str(round(getDeathProbablityOfNotQueerCharacters(df), 2)*100)+"%")
