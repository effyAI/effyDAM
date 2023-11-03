# Add new file to mongodb database with captions and keywords
import pymongo
from captioning import get_tags
from verify_keywords import new_hit

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]
        
def new_data(data):
    
    uid = data["uid"]
    s3_url = data["s3_url"]
    directory = data["directory"]
    file_type = data["type"]
    date = data["date"]
    time = data["time"]

    keywords, caption = get_tags(s3_url,file_type)
    
    send = {"uid":uid,"s3_url":s3_url,"dir":directory,"file_type":file_type, "keywords":keywords, "caption":caption, "date":date, "time":time}
    base_table.insert_one(send)

    new_hit(uid=uid, type = file_type, s3_url=s3_url,directory=directory, keywords=keywords)

    return {"output":"Data added sucessfully to the database"}
    
data = {
    "uid": 1,
    "s3_url": "https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg",
    "directory": "home/a",
    "type": "image",
    "date": "",
    "time": ""
}
