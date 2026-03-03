# ==========================================
# Malaria Detection - FINAL TRAINING SCRIPT
# ==========================================

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import json

# ==========================================
# SETTINGS
# ==========================================
dataset_dir = "dataset/train"
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 20

# ==========================================
# DATA GENERATOR (WITH PROPER PREPROCESSING)
# ==========================================
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,   # IMPORTANT
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="training"
)

val_generator = datagen.flow_from_directory(
    dataset_dir,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="binary",
    subset="validation"
)

# 🔥 PRINT CLASS INDICES (VERY IMPORTANT)
print("Class Indices:", train_generator.class_indices)

# Save class indices for Flask app
with open("class_indices.json", "w") as f:
    json.dump(train_generator.class_indices, f)

# ==========================================
# LOAD PRETRAINED MODEL
# ==========================================
base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(IMG_SIZE, IMG_SIZE, 3)
)

# Freeze most layers
base_model.trainable = True
for layer in base_model.layers[:-20]:
    layer.trainable = False

# ==========================================
# ADD CUSTOM CLASSIFIER
# ==========================================
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation="relu")(x)
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=output)

# ==========================================
# COMPILE MODEL
# ==========================================
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

model.summary()

# ==========================================
# CALLBACKS
# ==========================================
early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    "malaria_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max"
)

# ==========================================
# TRAIN MODEL
# ==========================================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=EPOCHS,
    callbacks=[early_stop, checkpoint]
)

print("✅ Model Training Completed and Best Model Saved!")

# ==========================================
# PLOT ACCURACY
# ==========================================
plt.figure()
plt.plot(history.history["accuracy"])
plt.plot(history.history["val_accuracy"])
plt.title("Model Accuracy")
plt.ylabel("Accuracy")
plt.xlabel("Epoch")
plt.legend(["Train", "Validation"])
plt.show()