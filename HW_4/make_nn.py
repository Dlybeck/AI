import os
import sys
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

def load_data(data_dir, validation_split=0.01):
    datagen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True,  #Flip images horizontally
    )
    filenames = os.listdir(data_dir)
    labels = []
    data = []

    for filename in filenames:
        if filename.startswith('c'):  #Label cat as 0
            label = 0
        elif filename.startswith('d'):  #Label dog as 1
            label = 1
        else:
            continue  #Ignore readme

        img_path = os.path.join(data_dir, filename)
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array) #array of all images
        labels.append(label) #array of all labels

    data = np.array(data) #Create numpy array for data
    labels = np.array(labels) #create numpy array for labels
    labels = to_categorical(labels, num_classes=2) #Converts to proper format. ex: [1, 0, 1] -> [[1, 0], [0, 1], [1, 0]]

    # Split the data into train and validation sets
    data_len = len(data)
    indices = np.arange(data_len) #create array of indices to shuffle
    np.random.shuffle(indices)
    split_index = int((1 - validation_split) * data_len) #find a random index to split the data

    x_train, x_val = data[:split_index], data[split_index:] #create training and vlidation set for for the images
    y_train, y_val = labels[:split_index], labels[split_index:] #create sets for labels

    batch_size = 20

    train_generator = datagen.flow(x_train, y_train, batch_size)
    val_generator = datagen.flow(x_val, y_val, batch_size)

    return train_generator, val_generator

def create_model():
<<<<<<< HEAD
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='tanh', input_shape=(100, 100, 3)),
        keras.layers.MaxPooling2D((5, 5)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Dropout(0.4),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='tanh'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(2, activation='softmax')  # Change to softmax and 2 output units
    ])

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])  # Change to categorical_crossentropy
=======
    #Layers:
    model = Sequential([
    Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(100, 100, 3)),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(64, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Conv2D(128, (3, 3), activation='relu', padding='same'),
    BatchNormalization(),
    MaxPooling2D((2, 2)),
    Dropout(0.25),
    
    Flatten(),
    Dense(256, activation='relu'),
    BatchNormalization(),
    Dropout(0.5),
    Dense(2, activation='softmax')
])
    
    optimizer = keras.optimizers.Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

>>>>>>> 0d1d396bfbb9d4cc713a3c84a7422934ec29fc23
    return model


data_dir = sys.argv[1] #get directory for images
model_filename = sys.argv[2] #get name of file to output

train_data, val_data = load_data(data_dir)

<<<<<<< HEAD
early_stopping_callback = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model = create_model()
model.fit(train_data, epochs=1000, validation_data=val_data, callbacks=[early_stopping_callback])

file_contents = model.to_json()

with open(model_filename + ".dnn", "w") as f:
    f.write(file_contents)
=======
#set up early stopping
early_stopping_callback = EarlyStopping(monitor='loss', patience=14, restore_best_weights=True)

model = create_model()
model.fit(train_data, epochs=1000, validation_data=val_data, callbacks=[early_stopping_callback])
>>>>>>> 0d1d396bfbb9d4cc713a3c84a7422934ec29fc23

#Save the model to an .h5 file
model.save(model_filename + ".h5",  include_optimizer = False)
print("Model saved to", model_filename, ".h5")