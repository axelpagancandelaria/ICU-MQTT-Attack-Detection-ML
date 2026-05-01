from openai import OpenAI
import pandas as pd
import json
import os

client = OpenAI(api_key="INSERT YOUR API KEY HERE")

df = pd.read_csv("PASTE YOUR OUTPUT FILE HERE")

normal = df[df["label"] == "normal"].sample(n=30, random_state=42)
flood = df[df["label"] == "flood"].sample(n=30, random_state=42)
slow = df[df["label"] == "slowite_like"].sample(n=30, random_state=42)

df = pd.concat([normal, flood, slow], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print("Total samples:", len(df))

samples = []

for i, row in df.iterrows():
    sample_text = {
        "id": i,
        "source_ip": str(row.get("ip.src", "unknown")),
        "destination_ip": str(row.get("ip.dst", "unknown")),
        "source_port": str(row.get("tcp.srcport", "unknown")),
        "destination_port": str(row.get("tcp.dstport", "unknown")),
        "frame_length": str(row.get("frame.len", "unknown")),
        "tcp_flags": str(row.get("tcp.flags", "unknown")),
        "mqtt_message_type": str(row.get("mqtt.msgtype", "unknown")),
        "mqtt_topic": str(row.get("mqtt.topic", "none"))
    }

    samples.append(sample_text)

prompt = f"""
You are a cybersecurity analyst classifying MQTT traffic from a simulated ICU network.

Normal context:
- 192.168.0.111 is an infusion pump
- 192.168.0.112 is a heart monitor
- 192.168.0.113 is a heart monitor
- 192.168.0.110 is the MQTT broker on port 1883
- 192.168.0.120 is an attacker used in the flood scenario

Classes:
- normal
- flood
- slowite_like

Rules:
- normal traffic usually comes from expected ICU devices and looks like regular MQTT publish traffic.
- flood traffic may involve high-volume attacker behavior or suspicious traffic from 192.168.0.120.
- slowite_like traffic may involve broker-local traffic, repeated connection behavior, reset/churn behavior, or unusual TCP behavior.

Classify each sample below.

Return ONLY valid JSON in this format:
[
  {{"id": 0, "prediction": "normal"}},
  {{"id": 1, "prediction": "flood"}}
]

Samples:
{json.dumps(samples, indent=2)}
"""

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0
)

answer = response.choices[0].message.content.strip()

print(answer)

predictions = json.loads(answer)

pred_df = pd.DataFrame(predictions)

df["true_label"] = df["label"]
df = df.merge(pred_df, left_index=True, right_on="id")

df = df.rename(columns={"prediction": "llm_prediction"})

df[["true_label", "llm_prediction"]].to_csv("gpt_batch_all_results.csv", index=False)

print("Saved gpt_batch_all_results.csv")