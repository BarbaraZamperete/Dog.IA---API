
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np


def pre_process_img(path):
    img = image.load_img(path, target_size=(299, 299))  # Tamanho padrão para Xception
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array



def breed (path, racas):
    model = load_model('D:/Bah/Documentos/ESTUDO/UFRR/TCC/TCC-Codes/dogia_django/dogia_app/ia/model/dog_breed_xception_part1.h5')
    
    img = pre_process_img(path)

    predictions = model.predict(img)
    predictions_list = [(score, racas[i+1]) for i, score in enumerate(predictions[0])]
    predictions_list.sort(reverse=True, key=lambda x: x[0])
    top = predictions_list[0]
    if (top[0] < 0.5):
        return (0, racas[0])
    else:
        return (top[0], top[1])
