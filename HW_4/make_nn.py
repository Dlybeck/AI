import os
import sys
import numpy as np
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping

# Function to load and preprocess images with class labels and split into train and validation sets
def load_data(data_dir, validation_split=0.2):
    datagen = ImageDataGenerator(rescale=1./255)
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

    # Split the data into train and validation sets
    num_samples = len(data)
    indices = np.arange(num_samples)
    np.random.shuffle(indices)
    split_index = int((1 - validation_split) * num_samples)

    x_train, x_val = data[:split_index], data[split_index:]
    y_train, y_val = labels[:split_index], labels[split_index:]

    train_generator = datagen.flow(x_train, y_train, batch_size=20)
    val_generator = datagen.flow(x_val, y_val, batch_size=20)

    return train_generator, val_generator

def create_model():  
    model = keras.Sequential([
        keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Conv2D(64, (3, 3), activation='relu'),
        keras.layers.Dropout(0.4),
        keras.layers.MaxPooling2D((2, 2)),
        keras.layers.Flatten(),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# Get data directory and output filename from command line arguments
data_dir = sys.argv[1]
model_filename = sys.argv[2]

# Load data with labels and split into train and validation sets
train_data, val_data = load_data(data_dir)

# Create the EarlyStopping callback
early_stopping_callback = EarlyStopping(monitor='val_accuracy', patience=2, restore_best_weights=True)

# Create and train the model
model = create_model()
model.fit(train_data, epochs=10, validation_data=val_data, callbacks=[early_stopping_callback])

# Save the model without optimizer information
file_contents = model.to_json()

with open(model_filename + ".dnn", "w") as f:
    f.write(file_contents)

print("Model saved to", model_filename, ".dnn")
