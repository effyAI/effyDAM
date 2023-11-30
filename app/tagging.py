from transformers import pipeline
import spacy
from ultralytics import YOLO
import cv2

nlp = spacy.load("en_core_web_sm")

blip = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
yolov8 = YOLO('development/effyDAM/app/yolov8x.pt', task = "predict")  # pretrained YOLOv8n model
names= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}

def words_from_sentence(sentence):
    word_list = []
    doc = nlp(sentence)
    for token in doc:
        if token.is_stop == False:
            word_list.append(token.lemma_)
    return word_list

def convert_to_range(lst):
    ranges = []
    start = lst[0]
    end = lst[0]

    for num in lst[1:]:
        if num == end + 1:
            end = num
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = num

    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ranges

def detect_file(source):
    objects =[]
    results = yolov8(source = source, stream = True, conf = 0.8)
    for result in results:
        id = result.boxes.cls
        for i in id:
            object = names[int(i)]
            if object not in objects:
                objects.append(object)        
    return objects      

def process_video(url):
    stamps = {}
    time_stamps = {}
    final_objects = []

    cap = cv2.VideoCapture(url)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = 0
    
    while True:
        success, frame = cap.read()
        if not success:
            break

        objects = detect_file(frame)
        temp = []
        if len(objects)!=0:
            for i in objects:
                if i not in final_objects:
                    final_objects.append(i)

                if i in temp:
                    objects.remove(i)
                else:
                    temp.append(i)
            stamps.update({frame_count:objects})

        frame_count += 1
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count * fps)

    cap.release() 

    for second, objects in stamps.items():
        for obj in objects:
            if obj in time_stamps: 
                time_stamps[obj].append(second)
            else:
                time_stamps[obj] = [second]
    
    for keyword, stamp in time_stamps.items():
        new_stamps = convert_to_range(stamp)
        time_stamps.update({keyword:new_stamps})

    # print(f"\nObjects: {final_objects}\n")
    # print(f"Stamps: {stamps}\n")
    # print(f"Detections: {time_stamps}\n")

    return final_objects, time_stamps

def process_image_or_video(s3_url, file_type):
    if file_type == "image":
        keywords = []
        cblip = blip(s3_url)[0]["generated_text"]
        caption = str(cblip)
        word_list = words_from_sentence(cblip)
        for i in word_list:
            if i not in keywords:
              keywords.append(i)
        yolo = detect_file(s3_url)
        for i in yolo:
            if i not in keywords:
                keywords.append(i)

        return keywords, caption, ""

    elif file_type == "video":
        caption = ""
        keywords , timestamps = process_video(s3_url) 
        return keywords, caption, timestamps


# v4 = "https://effy-dam.s3.amazonaws.com/production_id_3944832+(2160p).mp4"

# print(process_image_or_video(v4,"video"))

# print(get_tags("https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg","image"))
# print(convert_to_range([1,2,3,5,7,9,10,11,12,16,19,32,54, 66,67,68]))