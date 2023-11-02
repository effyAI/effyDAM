# Add new file to mongodb database with captions and keywords
import pymongo
from captioning import get_tags

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]


keyword_table = db["keyword_table"]



def new_data(data):
    
    uid = data["uid"]
    s3_url = data["s3_url"]
    dir = data["dir"]
    type = data["type"]

    keywords, caption = get_tags(s3_url,type)
    send = {"uid":uid,"s3_url":s3_url,"dir":dir,"file_type":type, "keywords":keywords, "caption":caption}
    add = base_table.insert_one(send)
    print(add)

    
    
# id,uid,s3_url, dir, type, keywords, caption