from ucimlrepo import fetch_ucirepo 
import pandas as pd

adult = fetch_ucirepo(id=2) 
df = pd.concat([adult.data.features, adult.data.targets], axis=1)  

#drop non QI columns
df = df.drop(columns=
        ["education", "income", "occupation", "relationship", "capital-gain", "education-num", "hours-per-week", "capital-loss", "fnlwgt"])

#fill blank and ? values with *
df = df.replace("?", "*")
df = df.replace(r"^\s*$", "*", regex=True)
df = df.fillna("*")

df.to_csv("csv/adult.csv", index=False)     
