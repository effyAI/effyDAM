from transformers import pipeline
import nltk
import spacy
from nltk import word_tokenize
import numpy as np
from ultralytics import YOLO
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

nlp = spacy.load("en_core_web_sm")

def process_text(sentence):
    word_list = []
    doc = nlp(sentence)
    for token in doc:
        if token.is_stop == False:
            word_list.append(token.lemma_)
    return word_list

blip = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device = device)
yolov8 = YOLO('yolov8x.pt', task = "detect")  # pretrained YOLOv8n model
names= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

def detect_file(source):
    objects=[]
    results = yolov8(source = source)
    for result in results:
        id = result.boxes.cls
        for i in id:
            object = names[int(i)]
            if object not in objects:
                objects.append(object)

    return objects

def get_tags(s3_url, file_type):
    if file_type == "image":
        keywords = []
        cblip = blip(s3_url)[0]["generated_text"]
        print(f"cblip")
        caption = str(cblip)
        processed = process_text(cblip)
        for i in processed:
            if i not in keywords:
              keywords.append(i)
        try:
            yolo = detect_file(s3_url)
            print(f"yolo")
        except:
            print("YOLO not working for image")
        for i in yolo:
            if i not in keywords:
                keywords.append(i)

        return keywords, caption

    elif file_type == "video":
        keywords=[]
        caption = ""
        try:
            yolo_det = detect_file(s3_url)
            print(f"yolo")
        except:
            print("YOLO not working for vid")

        for i in yolo_det:
            if i not in keywords:
                keywords.append(i)
        return keywords, caption
        


# print(get_tags("https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg","image"))