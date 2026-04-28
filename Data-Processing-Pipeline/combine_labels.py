#This script takes in normal, flood, and slowite CSV and combines it
#into one labeled data set used for model training.

import pandas as pd

#Loads the CSV files
normal = pd.read_csv("../Traffic_Data_Sets/icu_normal.csv")
flood = pd.read_csv("../Traffic_Data_Sets/icu_flood_attack.csv")
slow = pd.read_csv("../Traffic_Data_Sets/icu_slowite_attack.csv")

#Adds labels of each class
normal["label"] = "normal"
flood["label"] = "flood"
slow["label"] = "slowite_like"

#Combines all rows into one set
combined = pd.concat([normal, flood, slow], ignore_index=True)
combined.to_csv("../Traffic_Data_Sets/icu_combined_labeled.csv", index=False)

#Save the combined dataset
print("Saved icu_combined_labeled.csv")
print(combined["label"].value_counts())
print(combined.head())
