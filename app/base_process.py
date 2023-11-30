# Add new file to mongodb database with captions and keywords
import pymongo
from tagging import process_image_or_video
from new_data import new_hit
import os
from text_files import process_text_file
from audio_files import process_audio_file

open_file_types = ["psd","ai","esp","eps"]
text_file_types = ["txt","pdf","docx","xlsx"]
audio_file_types = ["mp3", "wav"]
image_video_file_types = ["jpg", "jpeg", "gif", "png", "mp4"]
all_types = []
all_types.extend(open_file_types)
all_types.extend(text_file_types)
all_types.extend(audio_file_types)
all_types.extend(image_video_file_types)

all_types_tuple = tuple(all_types)
print(all_types_tuple)

def remove_files_with_extensions(directory, extensions):
    for file in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file)):
            if file.endswith(extensions):
                os.remove(os.path.join(directory, file))

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]
        
def new_data(data):
    
    uuid = data["uid"]
    s3 = data["s3_url"]
    dir = data["directory"]
    file_type = data["type"]
    date = data["date"]
    time = data["time"]

    flag = 0
    if file_type == "image" or file_type == "video":
        keywords, caption, timestamps = process_image_or_video(s3,file_type)
        send = {"uid":uuid,"s3_url":s3,"dir":dir,"file_type":file_type, "keywords":keywords, "caption":caption, "timestamp": timestamps, "date":date, "time":time}
        add = base_table.insert_one(send)
        if not add:
            flag +=1
        x = new_hit(uid = uuid,file_type = file_type,s3_url = s3, directory=dir, keywords = keywords)
        if int(x):
            flag+=x
    
    elif file_type == "text":
        summary = process_text_file(s3)
        send = {"uid":uuid,"s3_url":s3,"dir":dir,"file_type":file_type, "keywords":[], "caption":summary, "timestamp": [], "date":date, "time":time}
        add = base_table.insert_one(send)    
    
    elif file_type == "audio":
        summary = process_audio_file(s3)
        send = {"uid":uuid,"s3_url":s3,"dir":dir,"file_type":file_type, "keywords":[], "caption":summary, "timestamp": [], "date":date, "time":time}
        add = base_table.insert_one(send)  
    
    remove_files_with_extensions("/home/ubuntu/development/effyDAM/app", all_types_tuple)
    
    if flag == 0:    
        return {"flag":0}
    else:
        return {"flag":1}
         
# data = {
#     "uid": 1,
#     "s3_url": "https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg",
#     "directory": "home/a",
#     "type": "image",
#     "date": "",
#     "time": ""
# }
