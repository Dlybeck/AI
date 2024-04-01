import tensorflow as tf
import cv2
import numpy as np

# Load the trained model
model = tf.keras.models.load_model("cat_dog_model.h5")

# Read the image to be tested
image = cv2.imread("test_image.jpg")

# Resize the image to the input shape of the model
image = cv2.resize(image, (150, 150))

# Convert the image to a numpy array and add an additional dimension
image = np.expand_dims(image, axis=0)

# Normalize the image
image = image / 255.0

# Make a prediction
predictions = model.predict(image)

# Get the class with the highest probability
class_index = np.argmax(predictions[0])

# Define the classes
classes = ["cat", "dog"]

# Print the predicted class
print("The model predicts that the image is a:", classes[class_index])