from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

# Dummy model architecture
def create_model():
    model = Sequential([
        Flatten(input_shape=(224, 224, 3)),
        Dense(64, activation="relu"),
        Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    return model

# Create and save models
acne_model = create_model()
pig_model = create_model()
mel_model = create_model()

acne_model.save("models/acne_model.h5")
pig_model.save("models/pigmentation_model.h5")
mel_model.save("models/melanoma_model.h5")

print("Dummy models created successfully!")
