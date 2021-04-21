"""Operations over datasets."""
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

from api.config import tfconfig


def create_dataset(from_path):
    """Create a dataset from a directory with images."""
    train_dataset = image_dataset_from_directory(
        from_path,
        validation_split=0.2,
        subset="training",
        seed=tfconfig.RANDOM_SEED,
        batch_size=tfconfig.BATCH_SIZE,
        image_size=tfconfig.IMG_SIZE,
        label_mode='categorical'
        )

    validation_dataset = image_dataset_from_directory(
        from_path,
        validation_split=0.2,
        subset="validation",
        seed=tfconfig.RANDOM_SEED,
        batch_size=tfconfig.BATCH_SIZE,
        image_size=tfconfig.IMG_SIZE,
        label_mode='categorical'
        )

    train_dataset = train_dataset.cache().shuffle(10, tfconfig.RANDOM_SEED)
    train_dataset = train_dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    validation_dataset = validation_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_dataset, validation_dataset
