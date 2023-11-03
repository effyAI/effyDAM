# Add new file to mongodb database with captions and keywords
import pymongo
from captioning import get_tags
import uuid

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]
keyword_table = db["keyword_table"]

#Base table data   {"uid":uid,"s3_url":s3_url,"dir":dir,"file_type":type, "keywords":keywords, "caption":caption

# Keyword Table Data
keyword_data =  {}   # {"keyword":[img_id,img_dir, vid_id, vid_dir]]}
keyword_find = keyword_table.find()

for doc in keyword_find:
    keyword = doc["keyword"]
    img_ids = doc["img_ids"]
    img_dirs = doc["img_dir"]
    vid_ids = doc["vid_ids"]
    vid_dirs = doc["vid_dir"]
    keyword_data.update({keyword:[img_ids,img_dirs,vid_ids,vid_dirs]})

def new_hit(uid,type,s3_url, directory,keywords):  # new_hit(uid=uid, type = type, s3_url=s3_url,directory=directory, keywords=keywords)
    for word in keywords:
        if word in keyword_data:
            # Found keyword , updating the existing one

            value = keyword_data.get(word)
            [im_ids,im_dirs, vi_ids, vi_dirs] = value
            
            filter = {"keyword":keyword}
            if type == "image":
                new_values = {"$set":{"img_ids":im_ids.append(uid), "image_dirs":im_dirs.append(directory)}}
                kt = keyword_table.update_one(filter=filter, update=new_values)
                if kt:
                    print("New data added to existing keyword.")
            elif type == "video":
                new_values = {"$set":{"vid_ids":vi_ids.append(uid), "image_dirs":vi_dirs.append(directory)}}
                kt = keyword_table.update_one(filter=filter, update=new_values)
                if kt:
                    print("New data added to existing keyword.")
        elif word not in keywords:
            # Creating a new keyword in the keyword table
            key_uuid = uuid.uuid4()
            uid_str = key_uuid.hex
            key_id = uid_str[:4]
            if type == 'image':
                img_ids = []
                img_dirs = []
                vid_ids = []
                vid_dirs = []
                img_ids.append(s3_url)
                img_dirs.append(directory)

                data ={"key_id":key_id,"keywords":keyword,"img_ids":img_ids, "image_dirs":img_dirs, "vid_ids":vid_ids, "vid_dirs":vid_dirs}
                kt = keyword_table.insert_one(data)
                if kt: 
                    print(f"New keyword added to keyword database: {keyword}")
            if type == 'video':
                img_ids = []
                img_dirs = []
                vid_ids = []
                vid_dirs = []
                vid_ids.append(s3_url)
                vid_dirs.append(directory)

                data ={"key_id":key_id,"keyword":keyword,"img_ids":img_ids, "img_dirs":img_dirs, "vid_ids":vid_ids, "vid_dirs":vid_dirs}
                kt = keyword_table.insert_one(data)
                if kt: 
                    print(f"New keyword added to keyword database: {keyword}")
        




                
