"""
Processes data from the dataset. Processes data from the dataset, removing irrelevant data in the spam text including 
punctuation, stop words, hyperlinks, etc. and representing the data as a feature matrix that allows the model 
architecture to effectively extract relationships between the sequence data and resulting label.
"""

import pandas as pd
import numpy as np
import string
import re
import os
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
DATASET = os.path.dirname(os.path.abspath(__file__)) + "/emails.csv"

data = pd.read_csv(DATASET)

text = data['text']
labels = data['spam']
labels_array = np.array(labels)

DATASET_SIZE = labels_array.shape[0]

DATA_DIR = 'data/'

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

cleaned_text_array = np.array([clean_pipeline(sentence) for sentence in text])
assert cleaned_text_array.shape == labels_array.shape

x_train, x_test = cleaned_text_array[:int(0.8 * DATASET_SIZE)], cleaned_text_array[int(0.8 * DATASET_SIZE):]
y_train, y_test = labels_array[:int(0.8 * DATASET_SIZE)], labels_array[int(0.8 * DATASET_SIZE):]

tokenizer = Tokenizer(num_words=MAX_FEATURE)

tokenizer.fit_on_texts(x_train)

x_train_features = pad_sequences(np.array(tokenizer.texts_to_sequences(x_train)), maxlen=MAX_LEN)
x_test_features = pad_sequences(np.array(tokenizer.texts_to_sequences(x_test)), maxlen=MAX_LEN)


if __name__ == '__main__':
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    mapping = {'x_train': x_train_features, 'x_test': x_test_features, 'y_train': y_train, 'y_test': y_test}

    for name, variable in mapping.items():
        print(f'{name} shape: {variable.shape}')
        np.save(f'{DATA_DIR}{name}.npy', variable)
    
    print(f'All data arrays saved to {DATA_DIR}')
