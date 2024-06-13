import numpy as np
import tensorflow as tf
import cv2
import os
from .funcao_perca import triplet, triplet_acc

PRETRAINED_MODEL = "D:/Bah/Documentos/ESTUDO/UFRR/TCC/TCC-Codes/dogia_django/dogia_app/ia/model/2019.07.29.dogfacenet.290.h5"

def embedding_creation(image):
    model = load_model()
    # print(path)
    # image = cv2.imread(path)
    resized_image = cv2.resize(image, (224,224))

    img_array = np.array(resized_image) / 255.0  # Normalização
    img_array = np.expand_dims(img_array, axis=0)  # Adicionar dimensão de batch
    q_embedding=model.predict(img_array)
    return q_embedding

def load_model():
    model = tf.keras.models.load_model(PRETRAINED_MODEL, custom_objects={'triplet': triplet, 'triplet_acc': triplet_acc})
    return model