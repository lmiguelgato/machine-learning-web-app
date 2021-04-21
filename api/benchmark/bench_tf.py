"""Benchmark to check TensorFlow is properly installed.
    
    Particularly useful for macs with Apple Silicon chips, where TensorFlow is not fully functional
    and stable yet.

    This benchmark consists of training a deep neural network, including two convolutional layers
    and two fully-connected layers, with max-pooling and dropout in between. It is the classical
    solution to the digits classifier for the MNIST dataset.

    The model is defined through the Sequential API from Keras, and the MNIST dataset is loaded
    from `tensorflow_datasets`: a collection of public research datasets that enable easy-to-use
    and high-performance input pipelines through the Data API from TensorFlow.

    Benchmark popularized thanks to this issue: https://github.com/apple/tensorflow_macos/issues/25"""
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import (
    Conv2D,
    MaxPooling2D,
    Dropout,
    Flatten,
    Dense
    )

# Set the global random seed for repeatability:
SEED = 42
tf.random.set_seed(SEED)

# Hyperparameters for training:
NUM_EPOCHS = 12
BATCH_SIZE = 128
LEARNING_RATE = 0.001

# Enable auto-tuning dataset operations:
AUTO = tf.data.experimental.AUTOTUNE

# Load MNIST dataset as `tf.data.Dataset` objects, and split it in train/test sets:
(ds_train, ds_test), ds_info = tfds.load(
    'mnist',
    split=['train', 'test'],
    as_supervised=True,
    with_info=True,
)


# Preprocessing function to keep images in the same scale and help gradient descent convergence:
def scale(image, label):
    """Normalizes and cast images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label


# Pipeline for the train dataset: preprocess, cache, shuffle, batch, and prefetch:
ds_train = ds_train.map(scale, num_parallel_calls=AUTO)  # autotune based on avail. CPU
ds_train = ds_train.cache()  # the 1st time the dataset is iterated over, its content will be cached
ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples, SEED)  # shuffles the dataset
ds_train = ds_train.batch(BATCH_SIZE)  # combine consecutive elements of this dataset into batches
ds_train = ds_train.prefetch(AUTO)  # autotune the buffer size when prefetching

# Do the same for the test dataset, except for shuffling since we're using the whole test set anyway
ds_test = ds_test.map(scale, num_parallel_calls=AUTO).cache().batch(BATCH_SIZE).prefetch(AUTO)

# Define a CNN through the Sequential API from Keras:
model = Sequential(
    [
        Conv2D(32, kernel_size=(3, 3), activation='relu'),
        Conv2D(64, kernel_size=(3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ]
    )

# Configure the model for training:
model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer=Adam(LEARNING_RATE),
    metrics=['accuracy'],
)

# Train and evaluate the model for `NUM_EPOCHS` iterations on the dataset:
model.fit(
    ds_train,
    epochs=NUM_EPOCHS,
    validation_data=ds_test,
)

# If left the model, dataset, seed, and hyperparameters unchanged, the classification accuracy at
# the end of the 12th epoch should be close to 85.27 % and 92.83 % on the training and test sets,
# respectively.
