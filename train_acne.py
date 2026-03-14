import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ==========================================
# 1️⃣ Dataset Path
# ==========================================

data_dir = "raw_acne"

# ==========================================
# 2️⃣ Data Generator (with preprocessing)
# ==========================================

datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=16,
    class_mode='categorical',
    subset='validation'
)

# ==========================================
# 3️⃣ Load Pretrained MobileNetV2
# ==========================================

base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

base_model.trainable = False   # Freeze base model

# ==========================================
# 4️⃣ Build Custom Top Layers
# ==========================================

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(train_generator.num_classes, activation='softmax')
])

# ==========================================
# 5️⃣ Compile
# ==========================================

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# 6️⃣ Train
# ==========================================

model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=10
)

# ==========================================
# 7️⃣ Save Model Permanently
# ==========================================

if not os.path.exists("models"):
    os.makedirs("models")

model.save("models/acne_model.keras")

print("✅ Acne MobileNet model trained and saved permanently!")