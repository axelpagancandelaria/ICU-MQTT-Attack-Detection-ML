import pandas as pd

normal = pd.read_csv("icu_normal.csv")
flood = pd.read_csv("icu_flood_attack.csv")
slow = pd.read_csv("icu_slowite_attack.csv")

normal["label"] = "normal"
flood["label"] = "flood"
slow["label"] = "slowite_like"

combined = pd.concat([normal, flood, slow], ignore_index=True)
combined.to_csv("icu_combined_labeled.csv", index=False)

print(combined["label"].value_counts())
print(combined.head())
