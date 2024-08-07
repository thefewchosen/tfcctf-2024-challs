import numpy as np
import tensorflow as tf
from PIL import Image

MODEL = tf.keras.models.load_model('./model.h5')
SIGNATURE_OK = 0


def predict(path):
    signature = tf.keras.utils.load_img(
        path,
        target_size=(96, 128),
        color_mode='grayscale',
        interpolation='bilinear',
    )
    signature = tf.keras.utils.img_to_array(signature)
    signature = np.array([signature]) / 255

    p = MODEL.predict(signature)[0][0]
    print(f'Prediction: {p}')
    status = round(p)

    # Only allow access if the signature is genuine
    if status == SIGNATURE_OK:
        return True
    else:
        return False
