# ICU-MQTT-Attack-Detection-ML

This project replicates an IoT healthcare network intrusion detection lab using MQTT traffic.  
It processes Wireshark captures, extracts features, and trains a Random Forest model to detect malicious traffic such as flood attacks and SlowITe-like attacks.

---

## 📁 Project Structure
ICU-MQTT-Attack-Detection-ML/
│
├── Traffic_Data_Sets/
│ ├── icu_normal.csv
│ ├── icu_flood_attack.csv
│ ├── icu_slowite_attack.csv
│ ├── icu_ml_ready.csv
│
├── Data-Processing-Pipeline/
│ ├── combine_labels.py
│ ├── prepare_features.py
│ ├── train_RandomForest.py
│ ├── results.py
│
└── README.md

---

## 🧠 What This Project Does

1. Takes MQTT traffic captured in Wireshark  
2. Converts it into structured CSV data  
3. Labels traffic as **normal or malicious**  
4. Builds features from the traffic  
5. Trains a **Random Forest model** to detect attacks  

---

## ⚙️ Requirements

Install dependencies:

```bash
pip install pandas scikit-learn numpy

If you get "externally managed environment", use:

python3 -m venv mqtt-env
source mqtt-env/bin/activate
pip install pandas scikit-learn numpy

##HOW TO RUN THE PIPELINNE

Step 1: Go into the processing directory
cd Data-Processing-Pipeline


Step 2: Combine and Label Data
python3 combine_labels.py

-This labels data as normal or malicious
-Loads CDV files from Traffic_Data_Sets
-Combines all datasets into one icu_ml_ready.csv


Step 3: Prepare Features
python3 prepare_features.py

-Cleans the data set
-Converts fields into features for ML


Step 4: Train the Model
python3 train_RandomForest.py

-Splits data into train/test
-Trains Random Forest Classifier
-Analyizes performance


Step 5: View Results
python3 results.py

-Prints accuracy, precision, recall and F1-score





