import os
import json
import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing import image
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.models import Model
import pyttsx3  # For text-to-speech

# Ensure TensorFlow is set to CPU mode only
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load word-index mappings
print("Loading word-to-index and index-to-word mappings...")
with open("data/textFiles/word_to_idx.pkl", 'rb') as file:
    word_to_index = pd.read_pickle(file, compression=None)

with open("data/textFiles/idx_to_word.pkl", 'rb') as file:
    index_to_word = pd.read_pickle(file, compression=None)

# Load the caption generation model
print("Loading the caption generation model...")
model = load_model('model_checkpoints/model_14.h5')

# Load the ResNet50 model for image feature extraction
print("Loading ResNet50 model...")
resnet50_model = ResNet50(weights='imagenet', input_shape=(224, 224, 3))
resnet50_model = Model(resnet50_model.input, resnet50_model.layers[-2].output)


def predict_caption(photo):
    """
    Generate a caption for the given photo using a greedy search algorithm.
    """
    inp_text = "startseq"

    for _ in range(80):  # Maximum caption length
        sequence = [word_to_index[w] for w in inp_text.split() if w in word_to_index]
        sequence = pad_sequences([sequence], maxlen=80, padding='post')

        ypred = model.predict([photo, sequence], verbose=0)  # Disable progress logging
        ypred = ypred.argmax()
        word = index_to_word.get(ypred, None)

        if word is None or word == 'endseq':
            break

        inp_text += ' ' + word

    # Remove startseq and endseq tokens
    final_caption = ' '.join(inp_text.split()[1:-1])
    return final_caption


def preprocess_image(img_path):
    """
    Preprocess an image to meet ResNet50 input requirements.
    """
    img = image.load_img(img_path, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)  # Convert 3D tensor to 4D tensor
    img = preprocess_input(img)  # Normalize image for ResNet50
    return img


def encode_image(img_path):
    """
    Encode an image into a feature vector using ResNet50.
    """
    img = preprocess_image(img_path)
    feature_vector = resnet50_model.predict(img, verbose=0)  # Disable progress logging
    return feature_vector


def text_to_speech(text):
    """
    Convert text to speech using pyttsx3.
    """
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speech rate
    engine.setProperty('volume', 0.9)  # Volume level
    engine.say(text)
    engine.runAndWait()


def runModel(img_name):
    """
    Main function to encode the image, generate a caption, and return it.
    """
    print("Encoding the image...")
    photo = encode_image(img_name).reshape((1, 2048))

    print("Running model to generate the caption...")
    caption = predict_caption(photo)

    print("Generated Caption:", caption)
    return caption
