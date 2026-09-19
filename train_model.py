import os
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# =========================
# SET SEED
# =========================
tf.random.set_seed(42)

# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

train_dir = os.path.join(BASE_DIR, "data", "Train")
test_dir = os.path.join(BASE_DIR, "data", "Test")
model_dir = os.path.join(BASE_DIR, "models")

os.makedirs(model_dir, exist_ok=True)

# =========================
# CHECK DATASET
# =========================
if not os.path.exists(train_dir):
    raise FileNotFoundError(f"Train folder not found: {train_dir}")

if not os.path.exists(test_dir):
    raise FileNotFoundError(f"Test folder not found: {test_dir}")

# =========================
# IMAGE SETTINGS
# =========================
img_size = (128, 128)
batch_size = 32

# =========================
# DATA GENERATOR
# =========================
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    shear_range=0.2
)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_data = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

test_data = test_datagen.flow_from_directory(
    test_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode="categorical"
)

# =========================
# SAVE CLASS INDICES
# =========================
class_indices_path = os.path.join(model_dir, "class_indices.json")

with open(class_indices_path, "w") as f:
    json.dump(train_data.class_indices, f)

print("✅ Class indices saved.")

# =========================
# BUILD MODEL
# =========================
model = Sequential([
    Input(shape=(128, 128, 3)),

    Conv2D(32, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Flatten(),

    Dense(128, activation="relu"),
    Dropout(0.5),

    Dense(train_data.num_classes, activation="softmax")
])

# =========================
# COMPILE MODEL
# =========================
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# =========================
# CALLBACKS
# =========================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=3,
    restore_best_weights=True,
    verbose=1
)

best_model_path = os.path.join(model_dir, "best_plant_disease_model.keras")

checkpoint = ModelCheckpoint(
    best_model_path,
    monitor="val_accuracy",
    save_best_only=True,
    verbose=1
)

# =========================
# TRAIN MODEL
# =========================
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=15,
    callbacks=[early_stop, checkpoint]
)

# =========================
# SAVE FINAL MODEL
# =========================
final_model_path = os.path.join(model_dir, "trained_plant_disease_model.keras")
model.save(final_model_path)

# =========================
# SAVE TRAINING HISTORY
# =========================
history_path = os.path.join(model_dir, "training_hist.json")

with open(history_path, "w") as f:
    json.dump(history.history, f)

print("\n✅ Model trained successfully.")
print(f"📁 Final Model Saved at: {final_model_path}")
print(f"📁 Best Model Saved at: {best_model_path}")
print(f"📁 Training History Saved at: {history_path}")