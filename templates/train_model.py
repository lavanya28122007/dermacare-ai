import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

def train_model(path, classes, model_name):
    img_size = (224,224)

    train = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True
    )

    val = ImageDataGenerator(rescale=1./255)

    train_data = train.flow_from_directory(
        path + "/train",
        target_size=img_size,
        class_mode='categorical'
    )

    val_data = val.flow_from_directory(
        path + "/val",
        target_size=img_size,
        class_mode='categorical'
    )

    base = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224,224,3))
    x = GlobalAveragePooling2D()(base.output)
    output = Dense(len(classes), activation='softmax')(x)

    model = Model(base.input, output)

    for layer in base.layers:
        layer.trainable = False

    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(train_data, validation_data=val_data, epochs=5)
    model.save("models/" + model_name + ".h5")

train_model("datasets/acne", ["low","moderate","high"], "acne_model")
train_model("datasets/melanoma", ["benign","malignant"], "melanoma_model")
train_model("datasets/pigmentation", ["low","moderate","high"], "pigmentation_model")
