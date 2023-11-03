# # Add new file to mongodb database with captions and keywords
# import pymongo

# client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
# db = client["effy-ai-tagging"]

# base_table = db["base_table"]
# keyword_table = db["keyword_table"]
# data ={"key_id":22,"keyword":"car","json_data":{},"directories":["a","b"], "image_ids":[213,232,5644,5643]}
# new ={"key_id":22,"keyword":"car","json_data":{},"directories":["a","b"], "image_ids":[0]}

# keyword_table.update_one(data,new)

# default = {
# }

# table = keyword_table.find()
# for values in table:
#     keyword = values["keyword"]
#     data=values["json_data"]
#     image_ids=values["image_ids"]
#     directories=values["directories"]
#     default.update({keyword:[image_ids,directories]})

# print(default)

a = ["abs"]

if type(a) == list:
    print(a)