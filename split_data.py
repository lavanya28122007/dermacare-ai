import os
import random
import shutil

source = "raw_acne"
dest = "."

def split_folder(src, dest, train=0.7, val=0.15, test=0.15):
    for split in ["train", "val", "test"]:
        os.makedirs(os.path.join(dest, split), exist_ok=True)

    for cls in os.listdir(src):
        cls_path = os.path.join(src, cls)
        if not os.path.isdir(cls_path):
            continue

        images = os.listdir(cls_path)
        random.shuffle(images)

        train_count = int(len(images) * train)
        val_count = int(len(images) * val)

        train_imgs = images[:train_count]
        val_imgs = images[train_count:train_count + val_count]
        test_imgs = images[train_count + val_count:]

        for split, img_list in [("train", train_imgs), ("val", val_imgs), ("test", test_imgs)]:
            split_cls_dir = os.path.join(dest, split, cls)
            os.makedirs(split_cls_dir, exist_ok=True)

            for img in img_list:
                shutil.copy(os.path.join(cls_path, img), os.path.join(split_cls_dir, img))

        print(f"{cls} -> train:{len(train_imgs)} val:{len(val_imgs)} test:{len(test_imgs)}")

split_folder(source, dest)
import os
import shutil
import random

def split_data(raw_folder, output_folder, train_ratio=0.7, val_ratio=0.2, test_ratio=0.1):
    classes = os.listdir(raw_folder)

    for cls in classes:
        cls_path = os.path.join(raw_folder, cls)
        images = os.listdir(cls_path)

        random.shuffle(images)

        train_end = int(len(images) * train_ratio)
        val_end = train_end + int(len(images) * val_ratio)

        train_images = images[:train_end]
        val_images = images[train_end:val_end]
        test_images = images[val_end:]

        for split, img_list in zip(["train", "val", "test"], [train_images, val_images, test_images]):
            split_folder = os.path.join(output_folder, split, cls)
            os.makedirs(split_folder, exist_ok=True)

            for img in img_list:
                src = os.path.join(cls_path, img)
                dst = os.path.join(split_folder, img)
                shutil.copy(src, dst)

raw_folder = "raw_pigmentation"
output_folder = "pigmentation_split"

split_data(raw_folder, output_folder)
print("Splitting Done!")
