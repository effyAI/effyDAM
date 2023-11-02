from transformers import pipeline
import nltk
import spacy
from nltk import word_tokenize,pos_tag, ne_chunk
import numpy as np
from ultralytics import YOLO
from nltk.corpus import stopwords
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

nltk.download("punkt")
nltk.download("stopwords")
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download("wordnet")

nlp = spacy.load("en_core_web_sm")

stemmer = nltk.stem.WordNetLemmatizer()

blip = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large", device = device)
yolov8 = YOLO('/content/model/yolov8x.pt')  # pretrained YOLOv8n model
names= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

# Run batched inference on a list of images
# model = YOLO('yolov5nu.pt')
def detect(source):
    objects=[]
    results = yolov8(source = source)
    for result in results:
        id = result.boxes.cls
        for i in id:
            object = names[int(i)]
            if object not in objects:
                objects.append(object)

    return objects

def process_text(sentence):
  text = stem(sentence.lower())
  tokens = word_tokenize(text)
  words = []
  stop_words = set(stopwords.words('english'))
  for i in tokens:
    if i not in stop_words and i.isalpha():
      words.append(i)
  return words

def stem(text):
    return stemmer.lemmatize(text.lower())

def get_tags(s3, type):
    keywords = []

    if type == "image":
        cblip = blip(s3)[0]["generated_text"]
        caption = str(cblip)
        processed = process_text(cblip)
        for i in processed:
            if i not in keywords:
              keywords.append(i)

        yolo = yolov8(s3)
        for i in yolo:
            if i not in keywords:
                keywords.append(i)

        return keywords, caption

    if type == "video":
        keywords=[]
        caption = []
        yolo_det = yolov8(s3)

        for i in yolo_det:
            if i not in keywords:
                keywords.append(i)
        data = {
            "keywords":keywords
        }
        return keywords, caption
        
