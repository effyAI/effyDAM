import pymongo
import spacy 

nlp = spacy.load("en_core_web_sm")

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

mycollection = db["keyword_table"]

keywords = []

def process_list(input_list):
    word_list = []
    for word in input_list:
        doc = nlp(word)
        for token in doc:
            if token.is_stop == False:
                word_list.append(token.lemma_)
        return word_list

for doc in mycollection.find():
    
    word = doc["keyword"]
    keywords.append(word)    


def get_data(input, filter):
    final_ids = []
    final_dirs = []
    word_list = process_list(input)
    
    if filter == None:
        for word in word_list:     
            if word in keywords:
                for doc in mycollection.find():
                    keyword = doc["keyword"]
                    img_ids = doc["img_ids"]
                    img_dirs = doc["img_dirs"]
                    vid_ids = doc["vid_ids"]
                    vid_dirs = doc["vid_dirs"]
                    
                    if keyword == word:
                        for i in img_ids:
                            if i not in final_ids:
                                final_ids.append(i)
                        for i in img_dirs:
                            if i not in final_dirs:
                                final_dirs.append(i)
                        for i in vid_ids:
                            if i not in final_ids:
                                final_ids.append(i)
                        for i in vid_dirs:
                            if i not in final_dirs:
                                final_dirs.append(i)

    elif filter == 'image':
        for word in word_list:     
            if word in keywords:
                for doc in mycollection.find():
                    keyword = doc["keyword"]
                    img_ids = doc["img_ids"]
                    img_dirs = doc["img_dirs"]                    
                    if keyword == word:
                        for i in img_ids:
                            if i not in final_ids:
                                final_ids.append(i)
                        for i in img_dirs:
                            if i not in final_dirs:
                                final_dirs.append(i)

    elif filter == 'video':
        for word in word_list:     
            if word in keywords:
                for doc in mycollection.find():
                    keyword = doc["keyword"]
                    vid_ids = doc["vid_ids"]
                    vid_dirs = doc["vid_dirs"]

                    for i in vid_ids:
                        if i not in final_ids:
                            final_ids.append(i)
                    for i in vid_dirs:
                        if i not in final_dirs:
                            final_dirs.append(i)
    
    
    return final_ids, final_dirs






def search(data, filter = None):
    
    input = data["data"]
    final_ids, final_dirs = get_data(input, filter)  
                        

    output = {
        "ids":final_ids,
        "directories":final_dirs      
    }

    return output


# datas = {"data":["person standing in fron of bus"]}

# print(search(datas))