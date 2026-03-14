import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ==========================================
# 1️⃣ Dataset Path
# ==========================================
data_dir = "raw_pigmentation"  # Replace with your folder path

# ==========================================
# 2️⃣ Data Generator (stronger augmentation)
# ==========================================
datagen = ImageDataGenerator(
    preprocessing_function=preprocess_input,
    validation_split=0.2,
    rotation_range=30,
    zoom_range=0.3,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,
    brightness_range=[0.7, 1.3]
)

train_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=32,  # Increased batch size for stability
    class_mode='categorical',
    subset='training'
)

val_generator = datagen.flow_from_directory(
    data_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

print(f"Training images: {train_generator.n}")
print(f"Validation images: {val_generator.n}")

# ==========================================
# 3️⃣ Load MobileNetV2
# ==========================================
base_model = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)
base_model.trainable = False  # Freeze initially

# ==========================================
# 4️⃣ Build Model with Extra Dropout
# ==========================================
x = layers.GlobalAveragePooling2D()(base_model.output)
x = layers.Dropout(0.5)(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.3)(x)
predictions = layers.Dense(train_generator.num_classes, activation='softmax')(x)

model = models.Model(inputs=base_model.input, outputs=predictions)

# ==========================================
# 5️⃣ Compile Model (initial training)
# ==========================================
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# ==========================================
# 6️⃣ Callbacks
# ==========================================
if not os.path.exists("models"):
    os.makedirs("models")

checkpoint = ModelCheckpoint(
    "models/best_pigmentation_model.keras",
    monitor="val_accuracy",
    save_best_only=True,
    mode="max"
)

early_stop = EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    patience=3,
    min_lr=1e-7,
    verbose=1
)

callbacks_list = [checkpoint, early_stop, reduce_lr]

# ==========================================
# 7️⃣ Train (initial phase with frozen base)
# ==========================================
history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,
    callbacks=callbacks_list
)

# ==========================================
# 8️⃣ Fine-tuning (unfreeze last 50 layers)
# ==========================================
base_model.trainable = True
for layer in base_model.layers[:-50]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(1e-5),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("🔓 Starting fine-tuning...")

history_ft = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=15,
    callbacks=callbacks_list
)

# ==========================================
# 9️⃣ Save Final Model
# ==========================================
model.save("models/pigmentation_model_final.keras")
print("✅ Pigmentation MobileNet model trained and saved!")