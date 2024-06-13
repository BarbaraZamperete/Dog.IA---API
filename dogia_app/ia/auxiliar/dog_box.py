import os
import cv2
import torch
import xml.etree.ElementTree as ET
from ultralytics import YOLO

# Função para detectar cachorros usando YOLOv8
def detect_dog(image_path, model_path):
    model = YOLO(model_path)
    results = model(image_path)
    for box in results[0].boxes:
        print(box)
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
            if cls == 16 and score > 0.5:  # 0 é a classe de cães no seu modelo YOLOv8
                object = ET.SubElement(root, "object")
                name = ET.SubElement(object, "name").text = "dog"
                bndbox = ET.SubElement(object, "bndbox")
                ET.SubElement(bndbox, "xmin").text = str(x_min)
                ET.SubElement(bndbox, "ymin").text = str(y_min)
                ET.SubElement(bndbox, "xmax").text = str(x_max)
                ET.SubElement(bndbox, "ymax").text = str(y_max)

    tree = ET.ElementTree(root)
    tree.write(output_xml)

# Caminho da imagem de entrada e arquivo XML de saída
image_path = "C:/Users/barbarazamperete/Documents/Barbara/TCC/Dog.IA---API/dogia_app/ia/auxiliar/terrier_yorkshire.3.1.jpeg"
model_path = 'C:/Users/barbarazamperete/Documents/Barbara/TCC/Dog.IA---API/dogia_app/ia/model/yolov8n.pt'  # Substitua pelo caminho do seu modelo YOLOv8
output_xml = 'output.xml'

# Detectar cachorros e gerar o arquivo XML
try:
    detections = detect_dog(image_path, model_path)
    create_xml(detections, image_path, output_xml)

    # Desenhar a caixa delimitadora na imagem e exibir (opcional)
    img = cv2.imread(image_path)
    for detection in detections:
        for box in detection.boxes:
            x_min, y_min, x_max, y_max = map(int, box.xyxy[0].tolist())
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

    cv2.imshow('Dog Detection', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(f"Ocorreu um erro: {e}")
