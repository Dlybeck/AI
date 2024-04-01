import os
import sys
import numpy as np
from tensorflow import keras

def classify_images(model_path, images_paths):
    # Load the pre-trained model
    model = keras.models.load_model(model_path)

    # Preprocess the images
    images = []
    for img_path in images_paths:
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        images.append(img_array)

    # Make predictions
    for img_path, img_array in zip(images_paths, images):
        prediction = model.predict(img_array)[0][0]
        if prediction < 0.5:
            class_name = 'cat'
        else:
            class_name = 'dog'
        print(f"{os.path.basename(img_path)}: {class_name}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python classify.py <model_path> <image1.jpg> <image2.jpg> ...")
        sys.exit(1)

    model_path = sys.argv[1]
    images_paths = sys.argv[2:]

    classify_images(model_path, images_paths)