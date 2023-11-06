# Add new file to mongodb database with captions and keywords
import pymongo
import uuid

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]


#Base table data   {"uid":uid,"s3_url":s3_url,"dir":dir,"file_type":type, "keywords":keywords, "caption":caption

# Keyword Table Data


def new_hit(uid,file_type,s3_url, directory,keywords):  # new_hit(uid=uid, type = type, s3_url=s3_url,directory=directory, keywords=keywords)
    flag = 0
    keyword_data =  []   # {"keyword":[img_id,img_dir, vid_id, vid_dir]]}
    
    keyword_table = db["keyword_table"]
    keyword_find = keyword_table.find()

    for doc in keyword_find:
        keyword = doc["keyword"]
        keyword_data.append(keyword)
    for word in keywords:
        if word not in keyword_data:
            # Creating a new keyword in the keyword table
            key_uuid = uuid.uuid4()
            uid_str = key_uuid.hex
            key_id = uid_str[:4]
            if file_type == 'image':
                img_ids = []
                img_dirs = []
                vid_ids = []
                vid_dirs = []
                img_ids.append(uid)
                img_dirs.append(directory)

                data_send ={"key_id":key_id,"keyword":word,"img_ids":img_ids, "img_dirs":img_dirs, "vid_ids":vid_ids, "vid_dirs":vid_dirs}
                kt = keyword_table.insert_one(data_send)
                if not kt:
                    flag += 1

            if file_type == 'video':
                img_ids = []
                img_dirs = []
                vid_ids = []
                vid_dirs = []
                vid_ids.append(uid)
                vid_dirs.append(directory)

                data_send ={"key_id":key_id,"keyword":word,"img_ids":img_ids, "img_dirs":img_dirs, "vid_ids":vid_ids, "vid_dirs":vid_dirs}
                kt1 = keyword_table.insert_one(data_send)
                if not kt1:
                    flag += 1
        
        elif word in keyword_data:
            # Found keyword , updating the existing one
            for doc in keyword_find:
                keyword = doc["keyword"]
                img_ids = doc["img_ids"]
                img_dirs = doc["img_dir"]
                vid_ids = doc["vid_ids"]
                vid_dirs = doc["vid_dir"]

                if word == keyword:
                    filter = {"keyword":keyword}
                    if file_type == "image":
                        new_values = {"$set":{"img_ids":img_ids.append(uid), "img_dirs":img_dirs.append(directory)}}
                        kt = keyword_table.update_one(filter=filter, update=new_values)
                        if not kt:
                            flag += 1
                    elif file_type == "video":
                        new_values = {"$set":{"vid_ids":vid_ids.append(uid), "vid_dirs":vid_dirs.append(directory)}}
                        kt = keyword_table.update_one(filter=filter, update=new_values)
                        if not kt:
                            flag += 1
                

    if flag == 0:
        return 0
    else:
        return 1

                