import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def load_data(data_dir):
    datagen = ImageDataGenerator(rescale=1./255)
    filenames = os.listdir(data_dir)
    labels = []
    data = []

    for filename in filenames:
        if filename.startswith('c'): #Cat image
            label = 0
        elif filename.startswith('d'): #Dog image
            label = 1
        else:
            continue #ignore Readme

        img_path = os.path.join(data_dir, filename)
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array)
        labels.append(label)

    data = np.array(data)
    labels = np.array(labels)

    return data, labels

def create_model(data_dir):
    data, labels = load_data(data_dir)

    # Set up early stopping
    early_stopping_callback = keras.callbacks.EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True)

    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Dropout(0.4),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(80, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model, data, labels, early_stopping_callback

#Get inputs
data_dir = sys.argv[1]
model_filename = sys.argv[2]

model, data, labels, early_stopping_callback = create_model(data_dir)

#Create and train the keras model
with tf.device('/gpu:0'):
    model.fit(data, labels, epochs=20, validation_split=0.2, callbacks=[early_stopping_callback])

# Save model as json file to later rename
file_contents = model.to_json()

# Set File type
f = open(model_filename + ".dnn", "w")
f.write(file_contents)
f.close()

print("Model saved to", model_filename, ".dnn")