# ICU-MQTT-Attack-Detection-ML

This project replicates an IoT healthcare network intrusion detection lab using MQTT traffic.  
It processes Wireshark captures, extracts features, and trains a Random Forest model to detect malicious traffic such as flood attacks and SlowITe-like attacks.

Iot-FLock was used to simulate;
-normal MQTT telemetry from medical devices
-MQTT publish flood traffic
-SlowITe-like broker stress behavior

Wireshark/tshark was then used to capture the traffic and export packet fields into csv format for preprocessing and machine learning

---

## 📁 Project Structure
ICU-MQTT-Attack-Detection-ML/
│
├── Traffic_Data_Sets/
│ ├── icu_normal.csv
│ ├── icu_flood_attack.csv
│ ├── icu_slowite_attack.csv
│ ├── icu_combined_labeled.csv
│ ├── icu_ml_ready.csv
│
├── Data-Processing-Pipeline/
│ ├── combine_labels.py
│ ├── prepare_features.py
│ ├── train_RandomForest.py
│ ├── detection.py
│
├── results/
│ ├── result_summary.txt
│ ├── feature_importances.csv
│
└── README.md

---

## 🧠 What This Project Does

1. Takes MQTT traffic captured in Wireshark  
2. Converts it into structured CSV data  
3. Labels traffic as **normal or malicious**  
4. Builds features from the traffic  
5. Trains a **Random Forest model** to detect attack
6. Supports live detection using 'tshark' and a saved trained model

---

## ⚙️ Requirements

##Reproducibility Note

The CSV datasets included in this repository are enough to reproduce the preprocessing and model-training 
pipeline without regenerating traffic. However, in order to run detection.py, a live traffic source is required.
In our project, Iot-Flock was used to generate that traffic and tshark was used to export the live packets fields
into `live_packets.csv` for the detection script. Additionally, the live detection is only reproducible for normal 
and flood traffic only. 

Install dependencies:

```bash
pip install pandas scikit-learn numpy joblib

If you get "externally managed environment", use:

python3 -m venv mqtt-env
source mqtt-env/bin/activate
pip install pandas scikit-learn numpy joblib

##HOW TO RUN THE PIPELINNE

Step 1: Go into the processing directory
cd Data-Processing-Pipeline


Step 2: Combine and Label Data
python3 combine_labels.py

-This labels data as normal or malicious
-Loads CSV files from Traffic_Data_Sets
-Combines all rows into icu_combined_labeled.csv


Step 3: Prepare Features
python3 prepare_features.py

-Cleans the data set
-Converts fields into features for ML
-Fills in the missing values
-Saves the dataset into icu_ml_ready.csv


Step 4: Train the Model
python3 train_RandomForest.py

-Loads icu_ml_ready.csv
-Splits data into train/test
-Trains Random Forest Classifier
-Analyizes performance
-Prints accuracy, precision, recall and F1-score

##LIVE DETECTION

Step 1: Start live packet capture with Tshark
run:
tshark -i any -Y "mqtt or tcp.port == 1883" -T fields \
-e frame.time_epoch \
-e ip.src \
-e ip.dst \
-e tcp.srcport \
-e tcp.dstport \
-e frame.len \
-e tcp.flags \
-e mqtt.msgtype \
-e mqtt.topic \
-E header=y -E separator=, -E occurrence=f \
> Traffic_Data_Sets/live_packets.csv

Step 2: Run the live detector
In another terminal:
cd Data-Processing-Pipeline
python3 detection.py

-This script reads the news live packets from live_packets.csv
-Preprocesses them to match the training 
-Loads the trained and saved model from rf_model_joblib
-Then predicts whethe the window is normal, flood, or slowite

--

## 📚Supporting Scholarly Articles
Anomaly Detection of Medical IoT Traffic Using Machine Learning
https://www.scitepress.org/Papers/2023/121320/121320.pdf
MalIoT: Scalable and Real-time Malware Traffic Detection for IoT Networks
https://arxiv.org/pdf/2304.00623



