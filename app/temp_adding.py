import pymongo

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]


# send = {"uid":234,"s3_url":"url","dir":"dir","file_type":"image", "keywords":["car"], "caption":"caption"}
# add = base_table.insert_one(send)

keyword_table = db["keyword_table"]

data ={"key_id":20,"keyword":"person", "img_ids":[0,1,2,3,4,5], "img_dir":["a","b","c","d","e"], "vid_ids":[200,201], "vid_dir":["a","b"] }

ket = keyword_table.insert_one(data)

# my_query = {"keyword":"bike"}

# new_values= {"$set":{"img_ids":[0,8,12], "img_dir":["a","b", "c","j", "m"], "vid_ids":[213,232,1,2]}}
# kt = keyword_table.update_one(filter=my_query, update=new_values)

