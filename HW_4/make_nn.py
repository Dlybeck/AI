import os
import sys
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Function to load and preprocess images with class labels
def load_data(data_dir):
  datagen = ImageDataGenerator(rescale=1./255)
  train_generator = datagen.flow_from_directory(
      data_dir,
      target_size=(100, 100),
      batch_size=32,  # Adjust batch size based on your GPU memory
      class_mode='binary'  # Binary classification (cat or dog)
  )
  # Extract labels from filenames (assuming 'c' for cat and 'd' for dog)
  labels = [os.path.basename(item)[0].lower() for item in train_generator.filenames]
  return train_generator, labels

def create_model():
  model = keras.Sequential([
      keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),  # Remove input_shape
      keras.layers.MaxPooling2D((2, 2)),
      keras.layers.Conv2D(64, (3, 3), activation='relu'),
      keras.layers.MaxPooling2D((2, 2)),
      keras.layers.Flatten(),
      keras.layers.Dense(64, activation='relu'),
      keras.layers.Dropout(0.5),
      keras.layers.Dense(1, activation='sigmoid')
  ])
  model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  return model


# Get data directory and output filename from command line arguments
data_dir = sys.argv[1]
model_filename = sys.argv[2]

# Load data with labels
train_data, labels = load_data(data_dir)

# Create and train the model
model = create_model()
model.fit(train_data, epochs=10, validation_data=(train_data, labels))  # Include validation data

# Save the model without optimizer information
model.save(model_filename, include_optimizer=False)

print("Model saved to", model_filename)
