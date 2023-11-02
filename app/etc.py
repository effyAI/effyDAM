# Add new file to mongodb database with captions and keywords
import pymongo

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

base_table = db["base_table"]
keyword_table = db["keyword_table"]

keywords = []
data = []
images = []
directories = []

table = keyword_table.find()
for values in table:
    keywords.append(values["keyword"])
    data.append(values["data"])
    images.append(values["images"])
    directories.append(values["directories"])

print(keywords, data, images, directories)