
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.xception import preprocess_input
import numpy as np

BREED_LIST = [
    'chihuahua', 'spaniel_japonês', 'cão_maltês', 'pequinês', 'shih_tzu', 'spaniel_blenheim', 'papillon',
    'terrier_de_bolso', 'ridgeback_do_rhodesia', 'cão_afegão', 'basset', 'beagle', 'bloodhound', 'bluetick', 'coonhound_preto_e_castanho', 'foxhound_americano',
    'foxhound_inglês', 'redbone', 'borzoi', 'wolfhound_irlandês', 'greyhound_italiano', 'whippet', 'podengo_ibicenco', 'elkhound_norueguês',
    'cão_de_lontra', 'saluki', 'deerhound_escocês', 'weimaraner', 'bullterrier_staffordshire', 'terrier_staffordshire_americano',
    'terrier_bedlington', 'terrier_border', 'terrier_azul_de_kerry', 'terrier_irlandês', 'terrier_norfolk', 'terrier_norwich',
    'terrier_yorkshire', 'fox_terrier_de_pelo_duro', 'terrier_lakeland', 'terrier_sealyham', 'airedale', 'cairn', 'terrier_australiano',
    'dinmont_dandie', 'bull_boston', 'schnauzer_miniatura', 'schnauzer_gigante', 'schnauzer_padrão', 'terrier_escocês',
    'terrier_tibetano', 'terrier_silky', 'terrier_de_revestimento_macio', 'terrier_branco_da_montanha_ocidental', 'lhasa_apso', 'retriever_de_revestimento_plano',
    'retriever_de_revestimento_encaracolado', 'retriever_dourado', 'retriever_labrador', 'retriever_da_baía_de_chesapeake', 'pointer_alemão_de_pelo_curto',
    'vizsla', 'setter_inglês', 'setter_irlandês', 'setter_gordon', 'spaniel_bretão', 'clumber_spaniel', 'springer_spaniel_inglês',
    'springer_spaniel_galês', 'spaniel_cocker', 'spaniel_sussex', 'spaniel_irlandês_d’água', 'kuvasz', 'schipperke', 'groenendael', 'malinois', 'briard', 'kelpie', 'komondor',
    'cão_de_pastoreio_antigo_inglês', 'cão_de_pastoreio_da_ilha_shetland', 'collie', 'collie_border', 'bouvier_dos_flandres', 'rottweiler',
    'pastor_alemão', 'doberman', 'pinscher_miniatura', 'cão_de_montanha_suíço', 'cão_de_montanha_bernês', 'appenzeller',
    'entlebucher', 'boxer', 'bullmastiff', 'mastim_tibetano', 'bulldog_francês', 'grande_dinamarquês', 'são_bernardo', 'cão_eskimo',
    'malamute', 'husky_siberiano', 'affenpinscher', 'basenji', 'pug', 'leonberg', 'terranova', 'grande_pirineus',
    'samoyed', 'pomerânia', 'chow_chow', 'keeshond', 'griffon_de_bruxelas', 'pembroke', 'cardigan', 'poodle_toy', 'poodle_miniatura',
    'poodle_padrão', 'cão_sem_pelo_mexicano', 'dingo', 'dhole', 'cão_caçador_africano'
]

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
    predictions_list = [(score, racas[i]) for i, score in enumerate(predictions[0])]
    predictions_list.sort(reverse=True, key=lambda x: x[0])
    # top = predictions_list[:10]
    top = predictions_list[0]
    print(top)
    # print(top[0])
    if (top[0] < 0.5):
        return (0, list(racas)[-1])
    else:
        return (top[0], top[1])
