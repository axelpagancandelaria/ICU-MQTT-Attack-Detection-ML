import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

df = pd.read_csv("icu_ml_ready.csv")

X = df.drop(columns=["label","frame.time_epoch"])
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
	X,y,
	test_size = 0.2,
	random_state = 42,
	stratify = y
)

rf = RandomForestClassifier(
	n_estimators = 100,
	random_state = 42,
	class_weight = "balanced"
)

rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred, output_dict = True)

with open("result_summary.txt", "w") as f:
	f.write(f"Accuracy: {acc}\n\n")
	f.write("Confusion Matrix:\n")
	f.write(str(cm))
	f.write("\n\nClassification Report:\n")
	f.write(pd.DataFrame(report).transpose().to_string())

importances = pd.Series(rf.feature_importances_, index = X.columns).sort_values(ascending = False)
importances.to_csv("feature_importances.csv", header =["importance"])

print("Saved result_summary.txt and feature_importances.csv")
