"""
Predicts whether emails are spam, using a loaded model. Allows integration of the model into the Dash application.
"""

from tensorflow.keras.models import save_model, load_model
import pandas as pd
import numpy as np
import string
import re
import os
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from process_data import tokenizer

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

DATA_DIR = 'data/'

MODEL_PATH = os.path.dirname(os.path.abspath(__file__)) + '/models/20200925163152_spam_classifier.h5'
DATASET = os.path.dirname(os.path.abspath(__file__)) + "/emails.csv"

EMBED_SIZE = 100 # word vector size
MAX_FEATURE = 50000 # number of unique words
MAX_LEN = 2000 # maximum number of words to use

### HELPER FUNCTIONS ###

def remove_hyperlinks(word):
    """Removes hyperlinks from a word"""
    return re.sub(r"http\S+", "", word)


def lower(word):
    """Sets all characters in a word to their lowercase value"""
    return word.lower()


def remove_numbers(word):
    """Removes all numbers from word"""
    return re.sub(r"\d+", '', word)


def remove_punctuation(word):
    """Removes all punctuation from word"""
    return word.translate(str.maketrans(dict.fromkeys(string.punctuation)))


def remove_whitespace(word):
    """Removes whitespace from word"""
    return word.strip()


def remove_newline(word):
    """Removes newline from word"""
    return word.replace('\n', '')


def clean_pipeline(sentence):
    """Apply cleaning functions in sequential order to an input sentence"""
    clean_utils = (remove_hyperlinks, remove_newline, lower, remove_numbers, remove_punctuation, remove_whitespace)
    for func in clean_utils:
        sentence = func(sentence)
    return sentence

### END HELPER FUNCTIONS ###
MODEL = load_model(MODEL_PATH, compile = True)

def predict(text, model):
    """
    Predicts whether <text> is spam or ham.

    Args:
        text (list): A list of text to predict.
        model: A model to use.

    Returns:
        A list of predictions
    """
    cleaned_text_array = np.array([clean_pipeline(sentence) for sentence in text])

    x = cleaned_text_array

    x_features = pad_sequences(np.array(tokenizer.texts_to_sequences(x)), maxlen=MAX_LEN)

    predictions = model.predict(x_features)
    predictions = [0 if output < 0.5 else 1 for output in predictions]

    return predictions


if __name__ == '__main__':

    # Test on the email dataset
    data = pd.read_csv(DATASET)
    text = data['text']

    predictions = predict(text, MODEL)
    print(predictions)
