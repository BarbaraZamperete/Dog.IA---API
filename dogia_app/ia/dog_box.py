import os
import cv2
import torch
import xml.etree.ElementTree as ET
from ultralytics import YOLO

MODEL = 'D:/Bah/Documentos/ESTUDO/UFRR/TCC/TCC-Codes/dogia_django/dogia_app/ia/model/yolov8n.pt'

# Função para detectar cachorros usando YOLOv8
def detect_dog(image_path):
    model = YOLO(MODEL)
    results = model(image_path)
    return results

# Função para criar um arquivo XML com os dados da caixa delimitadora
def create_xml(detections, image_path, output_xml):
    root = ET.Element("annotation")
    folder = ET.SubElement(root, "folder").text = "images"
    filename = ET.SubElement(root, "filename").text = os.path.basename(image_path)

    for detection in detections:
        for box in detection[0].boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())
            score = box.conf[0].item()
            cls = box.cls[0].item()
            object = ET.SubElement(root, "object")
            ET.SubElement(object, "name").text = "dog"
            ET.SubElement(object, "classe_yolo").text = str(cls)
            ET.SubElement(object, "confiabilidade_yolo").text = str(score)
            bndbox = ET.SubElement(object, "bndbox")
            ET.SubElement(bndbox, "xmin").text = str(x_min)
            ET.SubElement(bndbox, "ymin").text = str(y_min)
            ET.SubElement(bndbox, "xmax").text = str(x_max)
            ET.SubElement(bndbox, "ymax").text = str(y_max)

    tree = ET.ElementTree(root)
    tree.write(output_xml)

# Função para recortar a parte da imagem dentro da caixa delimitadora
def crop_img(detections, image):
    for detection in detections:
        for box in detection.boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())
            score = box.conf[0].item()
            cls = box.cls[0].item()
            if cls == 16 and score > 0.5:  # 16 é a classe de cães no seu modelo YOLOv8
                cropped_img = image[y_min:y_max, x_min:x_max]
                return cropped_img
            else: return image


# Função para criar a caixa delimitadora, recortar a imagem e criar o arquivo XML
def create_box(image_path, output_xml):
    detections = detect_dog(image_path)
    image = cv2.imread(image_path)

    cropped_images = crop_img(detections, image)
    create_xml(detections, image_path, output_xml)
    return cropped_images

