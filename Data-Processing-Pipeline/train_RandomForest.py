#This script trains and evaluates a Random Forest ML using the ICU
#dataset. It then prints the model accuracy and a confusion matrix
#with a report.

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

#Load the dataset
df = pd.read_csv("../Traffic_Data_Sets/icu_ml_ready.csv")

#This separates the features from the target label and drops the
#capture timestamps to avoid the ML from using those as part of detection
X = df.drop(columns=["label", "frame.time_epoch"])
y = df["label"]

#Splits the dataset into training and testing, while keeping
#a class balance in both sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

#Creates the ML
rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

#Training ML
rf.fit(X_train, y_train)

#Use the model to predict the labels for the testing set
y_pred = rf.predict(X_test)

#Prints the matrix, and the results
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

#Shows the most important features used by the model
importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nTop Feature Importances:")
print(importances.head(10))

# Save the trained model and feature column order
model_data = {
    "model": rf,
    "feature_columns": list(X.columns),
    "label_map": {0: "flood", 1: "normal", 2: "slowite_like"}
}
joblib.dump(model_data, "../Traffic_Data_Sets/rf_model.joblib")
print("\nSaved trained model to ../Traffic_Data_Sets/rf_model.joblib")
