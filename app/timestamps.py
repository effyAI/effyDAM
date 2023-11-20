import cv2
from ultralytics import YOLO
import time

yolov8 = YOLO('development/effyDAM/app/yolov8x.pt', task = "predict")  # pretrained YOLOv8n model
names= {0: 'person', 1: 'bicycle', 2: 'car', 3: 'motorcycle', 4: 'airplane', 5: 'bus', 6: 'train', 7: 'truck', 8: 'boat', 9: 'traffic light', 10: 'fire hydrant', 11: 'stop sign', 12: 'parking meter', 13: 'bench', 14: 'bird', 15: 'cat', 16: 'dog', 17: 'horse', 18: 'sheep', 19: 'cow', 20: 'elephant', 21: 'bear', 22: 'zebra', 23: 'giraffe', 24: 'backpack', 25: 'umbrella', 26: 'handbag', 27: 'tie', 28: 'suitcase', 29: 'frisbee', 30: 'skis', 31: 'snowboard', 32: 'sports ball', 33: 'kite', 34: 'baseball bat', 35: 'baseball glove', 36: 'skateboard', 37: 'surfboard', 38: 'tennis racket', 39: 'bottle', 40: 'wine glass', 41: 'cup', 42: 'fork', 43: 'knife', 44: 'spoon', 45: 'bowl', 46: 'banana', 47: 'apple', 48: 'sandwich', 49: 'orange', 50: 'broccoli', 51: 'carrot', 52: 'hot dog', 53: 'pizza', 54: 'donut', 55: 'cake', 56: 'chair', 57: 'couch', 58: 'potted plant', 59: 'bed', 60: 'dining table', 61: 'toilet', 62: 'tv', 63: 'laptop', 64: 'mouse', 65: 'remote', 66: 'keyboard', 67: 'cell phone', 68: 'microwave', 69: 'oven', 70: 'toaster', 71: 'sink', 72: 'refrigerator', 73: 'book', 74: 'clock', 75: 'vase', 76: 'scissors', 77: 'teddy bear', 78: 'hair drier', 79: 'toothbrush'}
ignore_ids = [29]
def detect_file(source):
    objects =[]
    results = yolov8(source = source, stream = True, conf = 0.5)
    for result in results:
        id = result.boxes.cls
        for i in id:
            if i not in ignore_ids:
                object = names[int(i)]
                if object not in objects:
                    objects.append(object)        
    return objects 

def process_video(url):
    # start_time = time.time()
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
    # print(default)

    # end_time = time.time()
    # elapsed_time = end_time - start_time
    # print(f"\nTime taken for timestamp process: {elapsed_time} seconds\n")
    # print(f"Objects: {final_objects}\n")
    # print(f"Stamps: {stamps}\n")
    # print(f"Detections: {time_stamps}\n")

    return final_objects, time_stamps


v1 = "https://effy-dam.s3.us-east-1.amazonaws.com/dam_1_93585_1699949543.mp4" 
v2 = "https://effy-dam.s3.amazonaws.com/production_id_3971609+(720p).mp4"  
v3 = "https://effy-dam.s3.amazonaws.com/test.mp4"
v4 = "https://effy-dam.s3.amazonaws.com/production_id_3944832+(2160p).mp4"

print(process_video(v4))


"""
V1      71 sec
{7: ['person'], 8: ['person'], 9: ['person'], 10: ['person'], 11: ['person', 'bottle'], 12: ['person'], 13: ['person'], 14: ['person'], 15: ['person'], 16: ['person'], 17: ['person'], 18: ['person'], 19: ['person'], 20: ['person'], 21: ['person'], 22: ['person', 'bottle'], 23: ['person'], 24: ['person', 'bottle'], 25: ['person'], 26: ['person', 'bottle'], 27: ['person'], 28: ['person'], 29: ['person'], 30: ['person'], 31: ['person'], 32: ['person'], 33: ['person'], 34: ['person'], 35: ['person'], 36: ['person'], 37: ['person', 'bottle'], 38: ['person'], 39: ['person', 'bottle'], 40: ['person'], 41: ['person'], 42: ['person'], 43: ['person'], 44: ['person'], 45: ['person'], 46: ['person'], 47: ['person'], 48: ['person', 'bottle'], 49: ['person'], 50: ['person'], 51: ['person'], 52: ['person'], 53: ['person'], 54: ['person'], 55: ['person'], 56: ['person'], 57: ['person', 'bottle'], 58: ['person'], 59: ['person'], 60: ['person'], 61: ['person', 'bottle'], 62: ['person'], 63: ['person', 'bottle'], 64: ['person'], 65: ['person'], 66: ['person'], 67: ['person'], 68: ['person'], 69: ['person'], 70: ['person'], 71: ['person'], 72: ['person', 'bottle'], 73: ['person'], 74: ['person'], 75: ['person'], 76: ['person'], 77: ['person'], 78: ['person'], 79: ['person'], 80: ['person'], 81: ['person'], 82: ['person'], 83: ['person'], 84: ['person'], 85: ['person'], 86: ['person']}

V2      10 sec
{0: ['keyboard', 'tv', 'mouse'], 1: ['mouse', 'tv', 'keyboard', 'laptop'], 2: ['mouse', 'keyboard', 'tv', 'laptop'], 3: ['mouse', 'keyboard', 'tv', 'laptop'], 4: ['mouse', 'tv', 'keyboard', 'laptop'], 5: ['mouse', 'tv', 'keyboard', 'laptop']}

V3      14 sec
{0: ['motorcycle', 'person'], 1: ['person', 'motorcycle'], 2: ['motorcycle', 'person'], 3: ['motorcycle', 'person'], 4: ['motorcycle', 'person'], 5: ['motorcycle', 'person'], 6: ['motorcycle', 'person'], 7: ['motorcycle', 'person'], 8: ['motorcycle'], 9: ['motorcycle']}

V4      16 sec 
{0: ['keyboard', 'mouse'], 1: ['keyboard', 'mouse', 'person'], 2: ['person', 'mouse', 'book', 'keyboard'], 3: ['keyboard', 'person', 'mouse'], 4: ['keyboard', 'person', 'mouse', 'book'], 5: ['keyboard', 'mouse'], 6: ['keyboard', 'mouse'], 7: ['keyboard', 'mouse']}

"""
