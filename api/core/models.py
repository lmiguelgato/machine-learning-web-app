"""Machine learning models and routines
"""
import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D


preprocess_input = tf.keras.applications.mobilenet_v2.preprocess_input
rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset=-1)
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])

mobile_net = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet')
# print(mobile_net.summary())

# TODO: define a class instead
inputs = tf.keras.Input(shape=(160, 160, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = mobile_net(x, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
outputs = Dense(3, activation='softmax')(x)

three_classes_classifier = tf.keras.Model(inputs, outputs)

""" image = Image.open(io.BytesIO(uri.data))
x = tf.keras.preprocessing.image.img_to_array(image)
print('--------------------', x.shape)
x = tf.image.resize(x, [160, 160])
print('--------------------', x.shape)
x = three_classes_classifier.predict(x[tf.newaxis, ...])
print('--------------------', x)
# print(three_classes_classifier.summary()) """
