import os
import sys
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import to_categorical

def load_data(data_dir, validation_split=0.01):
    datagen = ImageDataGenerator(
        rescale=1./255,
        horizontal_flip=True,  # Flip images horizontally
    )
    filenames = os.listdir(data_dir)
    labels = []
    data = []

    for filename in filenames:
        if filename.startswith('c'):  # Cat image
            label = 0
        elif filename.startswith('d'):  # Dog image
            label = 1
        else:
            continue  # Ignore files that don't start with 'c' or 'd'

        img_path = os.path.join(data_dir, filename)
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        data.append(img_array)
        labels.append(label)

    data = np.array(data)
    labels = np.array(labels)
    labels = to_categorical(labels, num_classes=2)  # One-hot encode the labels

    # Split the data into train and validation sets
    num_samples = len(data)
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    split_index = int((1 - validation_split) * num_samples)

    x_train, x_val = data[:split_index], data[split_index:]
    y_train, y_val = labels[:split_index], labels[split_index:]

    batch_size = 25

    train_generator = datagen.flow(x_train, y_train, batch_size)
    val_generator = datagen.flow(x_val, y_val, batch_size)

    return train_generator, val_generator

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization

def create_model():
    model = Sequential([
        Conv2D(64, (3, 3), padding='same', activation='relu', input_shape=(100, 100, 3)),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.3),
        
        Conv2D(128, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.4),
        
        Conv2D(256, (3, 3), padding='same', activation='relu'),
        BatchNormalization(),
        MaxPooling2D((2, 2)),
        Dropout(0.5),
        
        Flatten(),
        Dense(128, activation='relu'),
        BatchNormalization(),
        Dropout(0.3),
        
        Dense(2, activation='softmax')
    ])
    
    optimizer = keras.optimizers.Adam(learning_rate=0.0015)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    return model


data_dir = sys.argv[1]
model_filename = sys.argv[2]

train_data, val_data = load_data(data_dir)
early_stopping_callback = EarlyStopping(monitor='loss', patience=12, restore_best_weights=True)

model = create_model()
model.fit(train_data, epochs=1000, validation_data=val_data, callbacks=[early_stopping_callback])

# Save the model to an .h5 file
model.save(model_filename + ".h5")
print("Model saved to", model_filename, ".h5")