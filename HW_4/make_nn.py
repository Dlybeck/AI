import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

#Loads all needed data
def load_data(data_dir):
    datagen = ImageDataGenerator(rescale=1./255)
    filenames = os.listdir(data_dir)
    labels = []
    data = []

    for filename in filenames:
        if (filename.startswith('c')):  #Cat image
            label = 0
        elif (filename.startswith('d')):  #Dog image
            label = 1
        else:
            continue  #Ignore files that don't start with 'c' or 'd'

        img_path = os.path.join(data_dir, filename)
        #path = data_dir + "/" + filename?
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array)
        labels.append(label)

    data = np.array(data)
    labels = np.array(labels)

    #Split the data into train and validation sets
    training, validation, training_labels, validation_labels = train_test_split(data, labels, test_size=0.2, random_state=42)

    batch_size = 32

    train_generator = datagen.flow(training, training_labels, batch_size)
    val_generator = datagen.flow(validation, validation_labels, batch_size)

    return train_generator, val_generator

def create_model():
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
    return model

#get inputs
data_dir = sys.argv[1]
model_filename = sys.argv[2]

train_data, val_data = load_data(data_dir)

#Set up early stopping
early_stopping_callback = EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True)

#Create and train the keras model
with tf.device('/gpu:0'):
    model = create_model()

#run
with tf.device('/gpu:0'):
    model.fit(train_data, epochs=20, validation_data=val_data, callbacks=[early_stopping_callback])

#Save model as json file to later rename
file_contents = model.to_json()

#set File type
f = open(model_filename + ".dnn", "w")
f.write(file_contents)
f.close()

print("Model saved to", model_filename, ".dnn")