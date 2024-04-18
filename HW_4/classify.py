import os
import sys
import numpy as np
from tensorflow import keras

def classify_images(model_path, images_paths):
    model = keras.models.load_model(model_path)

    #Preprocess the images
    images = [] #create an array of properly formatted images (to make predictions off of)
    for img_path in images_paths:
        img = keras.preprocessing.image.load_img(img_path, target_size=(100, 100))
        img_array = keras.preprocessing.image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) #correct the model to have the correct shape
        images.append(img_array)

   #Make the predictions
    predictions = []
    for img in images:
        prediction = model.predict(img)[0]
        predictions.append(prediction)

    #add each prediction to an array in order
    names = []
    for prediction in predictions:
        class_index = np.argmax(prediction)
        if class_index == 0:
            name = 'cat'
        else:
            name = 'dog'
        names.append(name)

    #Print the classifications
    for i in range(len(images_paths)):
        img_path = images_paths[i]
        name = names[i]
        print(os.path.basename(img_path) + ": " + name)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Not enough arguments:\n python classify.py <model.h5> <image1> <image2> ...")
        sys.exit(1)

    model_path = sys.argv[1] #get path for the given model
    images_paths = sys.argv[2:] #get all images given
    classify_images(model_path, images_paths)