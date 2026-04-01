<<<<<<< HEAD
import os

base_dir = "raw_acne"   # your folder

for folder in ["acne_low", "acne_moderate", "acne_high"]:
    path = os.path.join(base_dir, folder)
    count = len([f for f in os.listdir(path) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    print(f"{folder} : {count} images")
=======
import os

base_dir = "raw_acne"   # your folder

for folder in ["acne_low", "acne_moderate", "acne_high"]:
    path = os.path.join(base_dir, folder)
    count = len([f for f in os.listdir(path) if f.lower().endswith((".jpg", ".jpeg", ".png"))])
    print(f"{folder} : {count} images")
>>>>>>> fc3d4d91f426282b7bbc9e8a0035378ac25b6974
