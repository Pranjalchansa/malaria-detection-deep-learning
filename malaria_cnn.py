# ==========================================
# MALARIA DETECTION USING CNN (FINAL VERSION)
# ==========================================

import os
import cv2
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns

from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.metrics import confusion_matrix, classification_report

# ==========================================
# 1. DATA DIRECTORIES
# ==========================================

train_dir = "Dataset/Train"
test_dir = "Dataset/Test"

categories = ["Parasite", "Uninfected"]

# ==========================================
# 2. DATA VISUALIZATION
# ==========================================

plt.figure(figsize=(10,5))

for i, category in enumerate(categories):
    path = os.path.join(train_dir, category)
    img_name = random.choice(os.listdir(path))
    img_path = os.path.join(path, img_name)

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    plt.subplot(1,2,i+1)
    plt.imshow(img)
    plt.title(category)
    plt.axis("off")

plt.show()

# ==========================================
# 3. DATA PREPROCESSING
# ==========================================

img_size = 128
batch_size = 32

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary'
)

val_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(img_size, img_size),
    batch_size=batch_size,
    class_mode='binary',
    shuffle=False
)

# ==========================================
# 4. BUILD CNN MODEL (IMPROVED)
# ==========================================

model = Sequential([
    Input(shape=(128,128,3)),

    Conv2D(32, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2,2),

    Conv2D(128, (3,3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ==========================================
# 5. TRAIN MODEL WITH EARLY STOPPING
# ==========================================

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,
    callbacks=[early_stop]
)

# ==========================================
# 6. PLOT ACCURACY & LOSS
# ==========================================

plt.figure(figsize=(12,5))

# Accuracy
plt.subplot(1,2,1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Model Accuracy")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend(["Train", "Validation"])

# Loss
plt.subplot(1,2,2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Model Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend(["Train", "Validation"])

plt.show()

# ==========================================
# 7. CONFUSION MATRIX
# ==========================================

val_generator.reset()
predictions = model.predict(val_generator)
y_pred = (predictions > 0.5).astype(int).reshape(-1)

cm = confusion_matrix(val_generator.classes, y_pred)

plt.figure(figsize=(6,6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

print("\nClassification Report:\n")
print(classification_report(val_generator.classes, y_pred))

# ==========================================
# 8. FEATURE MAP VISUALIZATION (KERAS 3 FIX)
# ==========================================

sample_path = os.path.join(train_dir, "Parasite")
sample_img_name = random.choice(os.listdir(sample_path))

sample_img = cv2.imread(os.path.join(sample_path, sample_img_name))
sample_img = cv2.resize(sample_img, (128,128))
sample_img = sample_img / 255.0
sample_img = np.reshape(sample_img, (1,128,128,3))

# Get first Conv2D layer safely
first_conv_layer = model.layers[1].output

activation_model = Model(
    inputs=model.inputs,   # ✅ FIXED HERE
    outputs=first_conv_layer
)

activation = activation_model.predict(sample_img)

plt.figure(figsize=(6,6))
plt.imshow(activation[0, :, :, 0], cmap='viridis')
plt.title("Feature Map - First Conv Layer")
plt.axis("off")
plt.show()