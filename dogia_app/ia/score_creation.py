from scipy.spatial.distance import euclidean, cosine
import numpy as np
import math

def distance_cal(emb_buscado, emb_avistado):

    np_buscado = np.array(emb_buscado)
    np_avistado = np.array(emb_avistado)

    distancia_euclidiana = euclidean(np_buscado, np_avistado)
    distancia_cosseno = cosine(np_buscado, np_avistado)

    return distancia_cosseno

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def score_creation(cachorro_buscado, cachorro_avistado, distancia):

    ind_g = (1 if cachorro_buscado.genero == cachorro_avistado.genero else 0.2)
    ind_b = (cachorro_buscado.raca_certeza if cachorro_buscado.raca == cachorro_avistado.raca else 0.5)

    return distancia * ind_g * ind_b