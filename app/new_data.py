# Add new file to mongodb database with captions and keywords
import pymongo
import uuid

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]
keyword_table = db["keyword_table"]


def new_hit(uid,file_type,s3_url, directory,keywords):  # new_hit(uid=uid, type = type, s3_url=s3_url,directory=directory, keywords=keywords)
    flag = 0
    keyword_data =  []   # {"keyword":[img_id,img_dir, vid_id, vid_dir]]}

    for doc in keyword_table.find():
        word1 = doc["keyword"]
        keyword_data.append(word1)

    for word in keywords:
        if word in keyword_data:
            # Found keyword , updating the existing one
            if file_type == "image":
                for doc in keyword_table.find():
                    keyword = doc["keyword"]
                    img_ids = doc["img_ids"]
                    img_dirs = doc["img_dirs"]
                    new_ids = img_ids
                    new_dirs = img_dirs
                    if uid not in new_ids:
                        new_ids.append(uid)
                    if directory not in new_dirs:
                        new_dirs.append(directory)
                    
                    if word == keyword:
                            filter = {"keyword":keyword}
                            new_values = {"$set":{"img_ids":new_ids, "img_dirs":new_dirs}}
                            kt = keyword_table.update_one(filter=filter, update=new_values)
                            if not kt:
                                flag += 1

            elif file_type == "video":
                for doc in keyword_table.find():
                    keyword = doc["keyword"]
                    vid_ids = doc["vid_ids"]
                    vid_dirs = doc["vid_dirs"]
                    new_ids2 = vid_ids
                    new_dirs2 = vid_dirs
                    if uid not in new_ids2:
                        new_ids2.append(uid)
                    if directory not in new_dirs2:
                        new_dirs2.append(directory)

                    if word == keyword:
                            filter2 = {"keyword":keyword}
                            new_values2 = {"$set":{"vid_ids":new_ids2, "vid_dirs":new_dirs2}}
                            kt = keyword_table.update_one(filter=filter2, update=new_values2)
                            if not kt:
                                flag += 1        
                        
        else:
            # Creating a new keyword in the keyword table
            key_uuid = uuid.uuid4()
            uid_str = key_uuid.hex
            key_id = uid_str[:4]
            if file_type == 'image':
                img_idss = []
                img_dirss = []
                vid_idss = []
                vid_dirss = []
                img_idss.append(uid)
                img_dirss.append(directory)

                data_send ={"key_id":key_id,"keyword":word,"img_ids":img_idss, "img_dirs":img_dirss, "vid_ids":vid_idss, "vid_dirs":vid_dirss}
                kt = keyword_table.insert_one(data_send)
                if not kt:
                    flag += 1

            elif file_type == 'video':
                img_idss = []
                img_dirss = []
                vid_idss = []
                vid_dirss = []
                vid_idss.append(uid)
                vid_dirss.append(directory)

                data_send ={"key_id":key_id,"keyword":word,"img_ids":img_idss, "img_dirs":img_dirss, "vid_ids":vid_idss, "vid_dirs":vid_dirss}
                kt1 = keyword_table.insert_one(data_send)
                if not kt1:
                    flag += 1  
                

    if flag == 0:
        return 0
    else:
        print("Flag raised to 1 for new hit file.py")
        return 1

                