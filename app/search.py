import pymongo

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

mycollection = db["keyword_table"]

images_data = {}
directory_data = {}

for row in mycollection.find():
    read   = row
    keyword = read["keyword"]
    images = read["images"]
    directories = read["directories"]

    images_data.update({keyword:images})
    directory_data.update({keyword:directories})

def get_images(word):
    if word in images_data:
        return images_data.get(word)

def get_directories(word):
    if word in directory_data:
        return directory_data.get(word)

def get_info(data):
    
    keyword = data["keyword"]
    
    output = {"images":get_images(keyword),"directories":get_directories(keyword) }

    return output 