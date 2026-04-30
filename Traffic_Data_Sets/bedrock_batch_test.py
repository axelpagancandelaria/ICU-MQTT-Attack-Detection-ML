import boto3
import pandas as pd
import time
from botocore.exceptions import ClientError

client = boto3.client("bedrock-runtime", region_name="us-east-1")

MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

df = pd.read_csv("icu_combined_labeled.csv")

normal = df[df["label"] == "normal"].sample(n=30, random_state=42)
flood = df[df["label"] == "flood"].sample(n=30, random_state=42)
slow = df[df["label"] == "slowite_like"].sample(n=30, random_state=42)

df = pd.concat([normal, flood, slow], ignore_index=True)

df["traffic_summary"] = (
    "Source IP: " + df["ip.src"].astype(str) +
    "\nDestination IP: " + df["ip.dst"].astype(str) +
    "\nSource Port: " + df["tcp.srcport"].astype(str) +
    "\nDestination Port: " + df["tcp.dstport"].astype(str) +
    "\nFrame Length: " + df["frame.len"].astype(str) +
    "\nTCP Flags: " + df["tcp.flags"].astype(str) +
    "\nMQTT Message Type: " + df["mqtt.msgtype"].astype(str) +
    "\nMQTT Topic: " + df["mqtt.topic"].astype(str)
)

def classify(summary):
    prompt = f"""
You are a cybersecurity analyst for a simulated ICU MQTT network.

Normal context:
- 192.168.0.111 is an infusion pump
- 192.168.0.112 is a heart monitor
- 192.168.0.113 is an oxygen sensor
- 192.168.0.110 is the MQTT broker on port 1883

Classify this MQTT traffic as exactly one of:
normal
flood
slowite_like

Traffic Summary:
{summary}

Answer with ONLY the class.
"""

    for attempt in range(5):
        try:
            response = client.converse(
                modelId=MODEL_ID,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                inferenceConfig={
                    "maxTokens": 50,
                    "temperature": 0
                }
            )

            return response["output"]["message"]["content"][0]["text"].strip().lower()

        except ClientError as e:
            error_code = e.response["Error"]["Code"]

            if error_code == "ThrottlingException":
                wait_time = 5 * (attempt + 1)
                print(f"Throttled. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise

    return "error"

results = []

for i, row in df.iterrows():
    print(f"Running {i+1}/{len(df)}")

    pred = classify(row["traffic_summary"])

    results.append({
        "true_label": row["label"],
        "llm_prediction": pred,
        "traffic_summary": row["traffic_summary"]
    })

    time.sleep(2)

out = pd.DataFrame(results)
out.to_csv("llm_results.csv", index=False)

print("Saved llm_results.csv")