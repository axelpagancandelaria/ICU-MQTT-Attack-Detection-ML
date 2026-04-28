#This script prepares the ICU combined dataset into a dataset better
#fit for machine learning. It fills in the missing values and turns
#text files into number codes.

import pandas as pd

#Load combined dataset
df = pd.read_csv("../Traffic_Data_Sets/icu_combined_labeled.csv")

#Fill in the missing values so it doesn't crash
df["mqtt.topic"] = df["mqtt.topic"].fillna("NONE")
df["mqtt.msgtype"] = df["mqtt.msgtype"].fillna(-1)
df["tcp.flags"] = df["tcp.flags"].fillna("0x0000")
df["tcp.srcport"] = df["tcp.srcport"].fillna(0)
df["tcp.dstport"] = df["tcp.dstport"].fillna(0)
df["ip.src"] = df["ip.src"].fillna("0.0.0.0")
df["ip.dst"] = df["ip.dst"].fillna("0.0.0.0")

#Makes a copy to keep the original
clean = df.copy()

#Converts the texts columns into number codes for easier ML reading

for col in ["ip.src", "ip.dst", "tcp.flags", "mqtt.topic", "label"]:
    clean[col] = clean[col].astype("category").cat.codes

#Saves the dataset
clean.to_csv("../Traffic_Data_Sets/icu_ml_ready.csv", index=False)

#Print confirmation
print("Saved icu_ml_ready.csv")
print(clean.head())
print(clean.shape)
