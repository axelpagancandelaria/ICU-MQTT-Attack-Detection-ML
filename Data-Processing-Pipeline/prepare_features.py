import pandas as pd

df = pd.read_csv("icu_combined_labeled.csv")

df["mqtt.topic"] = df["mqtt.topic"].fillna("NONE")
df["mqtt.msgtype"] = df["mqtt.msgtype"].fillna(-1)
df["tcp.flags"] = df["tcp.flags"].fillna("0x0000")
df["tcp.srcport"] = df["tcp.srcport"].fillna(0)
df["tcp.dstport"] = df["tcp.dstport"].fillna(0)
df["ip.src"] = df["ip.src"].fillna("0.0.0.0")
df["ip.dst"] = df["ip.dst"].fillna("0.0.0.0")

clean = df.copy()

for col in ["ip.src", "ip.dst", "tcp.flags", "mqtt.topic", "label"]:
    clean[col] = clean[col].astype("category").cat.codes

clean.to_csv("icu_ml_ready.csv", index=False)

print("Saved icu_ml_ready.csv")
print(clean.head())
print(clean.shape)
