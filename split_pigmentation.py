import os
import shutil
import random

# Source folder
SOURCE_DIR = "raw_pigmentation"

# Target folders
TRAIN_DIR = "train/pigmentation"
VAL_DIR = "val/pigmentation"

# Create folders
for folder in ["low", "moderate", "high"]:
    os.makedirs(os.path.join(TRAIN_DIR, folder), exist_ok=True)
    os.makedirs(os.path.join(VAL_DIR, folder), exist_ok=True)

# Mapping raw folder names to class names
folder_map = {
    "pigmentation_low": "low",
    "pigmentation_moderate": "moderate",
    "pigmentation_high": "high"
}

# Split ratio
SPLIT_RATIO = 0.8

for raw_folder, class_name in folder_map.items():
    path = os.path.join(SOURCE_DIR, raw_folder)
    images = os.listdir(path)
    random.shuffle(images)

    split_index = int(len(images) * SPLIT_RATIO)

    train_images = images[:split_index]
    val_images = images[split_index:]

    for img in train_images:
        shutil.copy(os.path.join(path, img),
                    os.path.join(TRAIN_DIR, class_name, img))

    for img in val_images:
        shutil.copy(os.path.join(path, img),
                    os.path.join(VAL_DIR, class_name, img))

print("✅ Pigmentation data split completed!")
