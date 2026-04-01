<<<<<<< HEAD
# model_loader.py
from tensorflow.keras.models import load_model
import os

MODEL_DIR = "models"

def load_acne_model():
    path = os.path.join(MODEL_DIR, "acne_model.keras")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Acne model not found at {path}")
    return load_model(path)

def load_pigmentation_model():
    path = os.path.join(MODEL_DIR, "best_pigmentation_model.keras")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pigmentation model not found at {path}")
    return load_model(path)

def load_melanoma_model():
    path = "models/melanoma_model.keras"  # use this existing file
    if not os.path.exists(path):
        raise FileNotFoundError(f"Melanoma model not found at {path}")
=======
# model_loader.py
from tensorflow.keras.models import load_model
import os

MODEL_DIR = "models"

def load_acne_model():
    path = os.path.join(MODEL_DIR, "acne_model.keras")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Acne model not found at {path}")
    return load_model(path)

def load_pigmentation_model():
    path = os.path.join(MODEL_DIR, "best_pigmentation_model.keras")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pigmentation model not found at {path}")
    return load_model(path)

def load_melanoma_model():
    path = "models/melanoma_model.keras"  # use this existing file
    if not os.path.exists(path):
        raise FileNotFoundError(f"Melanoma model not found at {path}")
>>>>>>> fc3d4d91f426282b7bbc9e8a0035378ac25b6974
    return load_model(path)