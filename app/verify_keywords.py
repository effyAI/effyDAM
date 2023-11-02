# Add new file to mongodb database with captions and keywords
import pymongo
from captioning import get_tags
import uuid

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]
keyword_table = db["keyword_table"]

existing_keywords = []


keyword_find = keyword_table.find()
for value in keyword_find:
    keyword = value["keyword"]
    existing_keywords.append(keyword)


def verify(keywords, file_id):
    for keyword in keywords:
        if keyword not in existing_keywords:
            uid = uuid.uuid4()
            uid_str = uid.hex
            unique_id = uid_str[:4]
            directory = ""
            data ={"kid":unique_id,"keywords":keyword,"json_data":"","directory":"", "image_id":file_id}
        