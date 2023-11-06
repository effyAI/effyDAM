# Add new file to mongodb database with captions and keywords
import pymongo
from captioning import get_tags
from verify_keywords import new_hit
import subprocess

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

    keywords, caption = get_tags(s3,file_type)
    send = {"uid":uuid,"s3_url":s3,"dir":dir,"file_type":file_type, "keywords":keywords, "caption":caption, "date":date, "time":time}
    add = base_table.insert_one(send)
    if not add:
        flag +=1
    x = new_hit(uid = uuid,file_type = file_type,s3_url = s3, directory=dir, keywords = keywords)
    if x  == 0 and flag == 0:
        return "Successfully added to database"
    else:
        return "Not successfully added to database"
# data = {
#     "uid": 1,
#     "s3_url": "https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg",
#     "directory": "home/a",
#     "type": "image",
#     "date": "",
#     "time": ""
# }
