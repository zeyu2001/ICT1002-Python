import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation, Bidirectional

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

DATA_DIR = 'data/'
MODEL_DIR = 'models/'
METRICS_DIR = 'metrics/'

DIRS = (DATA_DIR, MODEL_DIR, METRICS_DIR)

for directory in DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)

MAX_FEATURE = 50000 # number of unique words
MAX_LEN = 2000 # maximum number of words to use
EMBEDDING_VECTOR_LENGTH = 32

TRAIN_PARAMS = {"batch_size": 512, "epochs": 20}

x_train = np.load(f'{DATA_DIR}/x_train.npy')
x_test = np.load(f'{DATA_DIR}/x_test.npy')
y_train = np.load(f'{DATA_DIR}/y_train.npy')
y_test = np.load(f'{DATA_DIR}/y_test.npy')

classifier = Sequential(
    [
        Embedding(MAX_FEATURE, EMBEDDING_VECTOR_LENGTH, input_length=MAX_LEN), # input_dim, output_dim
        Bidirectional(LSTM(64)),
        Dense(16, activation='relu'),
        Dropout(0.1),
        Dense(1, activation='sigmoid'),
    ]
    )

classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# classifier.summary()

if __name__ == '__main__':
    now = datetime.now().strftime('%Y%m%d%H%M%S')
    model_filename = now + '_spam_classifier.h5'
    accplot_filename = now + '_plot.png'

    history = classifier.fit(x_train, y_train, validation_data=(x_test, y_test), **TRAIN_PARAMS)

    classifier.save(f'{MODEL_DIR}{model_filename}')

    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.grid()
    plt.savefig(f'{METRICS_DIR}{accplot_filename}')

