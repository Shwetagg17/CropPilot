import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder

# MODELS
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score, classification_report

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("Crop_recommendation.csv")

X = df.drop("label", axis=1)
y = df["label"]

# =========================
# ENCODE LABEL
# =========================
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# =========================
# TRAIN TEST SPLIT
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# =========================
# SCALING
# =========================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =========================
# DEFINE MODELS
# =========================
models = {
    "RandomForest": RandomForestClassifier(),
    "DecisionTree": DecisionTreeClassifier(),
    "KNN": KNeighborsClassifier(),
    "SVM": SVC(probability=True)
}

# =========================
# TRAIN + EVALUATE
# =========================
best_model = None
best_accuracy = 0
best_model_name = ""

print("\n========== TRAINING MODELS ==========\n")

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    preds = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, preds)

    print(f"{name} Accuracy: {acc * 100:.2f}% ({acc:.4f})")

    if acc > best_accuracy:
        best_accuracy = acc
        best_model = model
        best_model_name = name

# =========================
# BEST MODEL RESULT
# =========================
print("\n========== BEST MODEL ==========\n")
print(f"Best Model: {best_model_name}")
print(f"Best Accuracy: {best_accuracy * 100:.2f}%")

# =========================
# DETAILED REPORT
# =========================
final_preds = best_model.predict(X_test_scaled)

print("\n========== CLASSIFICATION REPORT ==========\n")
print(classification_report(y_test, final_preds))

# =========================
# SAVE MODEL FILES
# =========================
pickle.dump(best_model, open("crop_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
pickle.dump(le, open("label_encoder.pkl", "wb"))

print("\n✅ Crop Model saved successfully!")