import pandas as pd

# Change this file depending on model:
# "llm_results.csv" for Claude
# "nova_lite_results.csv" for Nova
df = pd.read_csv("gpt_results.csv")

def extract_class(text):
    text = str(text).lower()

    if "slowite" in text:
        return "slowite_like"
    elif "flood" in text:
        return "flood"
    elif "normal" in text:
        return "normal"
    else:
        return "unknown"

df["llm_prediction_clean"] = df["llm_prediction"].apply(extract_class)

y_true = df["true_label"]
y_pred = df["llm_prediction_clean"]

classes = ["flood", "normal", "slowite_like"]

correct = (y_true == y_pred).sum()
total = len(df)
accuracy = correct / total

print("Accuracy:", accuracy)

print("\nConfusion Matrix:")
matrix = pd.crosstab(
    y_true,
    y_pred,
    rownames=["Actual"],
    colnames=["Predicted"],
    dropna=False
)

matrix = matrix.reindex(index=classes, columns=classes, fill_value=0)
print(matrix)

print("\nClassification Report:")

for cls in classes:
    tp = ((y_true == cls) & (y_pred == cls)).sum()
    fp = ((y_true != cls) & (y_pred == cls)).sum()
    fn = ((y_true == cls) & (y_pred != cls)).sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0
    support = (y_true == cls).sum()

    print(f"{cls:15} precision={precision:.2f} recall={recall:.2f} f1-score={f1:.2f} support={support}")

df.to_csv("llm_evaluated.csv", index=False)

print("\nSaved llm_evaluated.csv")