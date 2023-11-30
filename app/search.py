import pymongo
import spacy 

nlp = spacy.load("en_core_web_sm")

client = pymongo.MongoClient("mongodb+srv://effybizai:AhM2SPj8dKfLId89@cluster0.yfq6agh.mongodb.net/?retryWrites=true&w=majority")
db = client["effy-ai-tagging"]

mycollection = db["keyword_table"]


def process_list(input_list):
    word_list = []
    for word in input_list:
        doc = nlp(word)
        for token in doc:
            if token.is_stop == False:
                word_list.append(token.lemma_)
        return word_list

def get_data(input, filter):
    keywords = []
    keyword_data = {}
    
    for doc in mycollection.find():
        word = doc["keyword"]
        keywords.append(word)    
    
    word_list = process_list(input)
    
    if filter == None:
        for word in word_list: 
            final_ids = []
            final_dirs = []    
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

                keyword_data.update({word:{"ids":final_ids, "dirs":final_dirs}})
            else:
                keyword_data.update({word:{"ids":[], "dirs":[]}})
    

    elif filter == 'image':
        for word in word_list:   
            final_ids = []
            final_dirs = []   
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
                keyword_data.update({word:{"ids":final_ids, "dirs":final_dirs}})
            else:
                keyword_data.update({word:{"ids":[], "dirs":[]}})   
    elif filter == 'video':
        for word in word_list:
            final_ids = []
            final_dirs = []      
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
                keyword_data.update({word:{"ids":final_ids, "dirs":final_dirs}})
            else:
                keyword_data.update({word:{"ids":[], "dirs":[]}}) 
    print(keyword_data)    
    
    return keyword_data

def search(data, filter = None):
    
    input = data["data"]
    # final_ids, final_dirs = get_data(input, filter)  

    # output = {
    #     "ids":final_ids,
    #     "directories":final_dirs      
    # }
    output = get_data(input, filter)                      

    return output


# datas = {"data":["person standing in front of bus"]}

# print(search(datas))



# {'person': {'ids': ['509', '510', 2729222222, 509, 525, '526', 533, '535', '536', '537', '559', '1', '2', '3', '4', 2983648, 291122111, 545212, 5452122222222, 5488888, 5488, 54232323232323, '534', '540', '6'], 'dirs': ['https://demo.effybiz.com/temp/', 'home/c', 'https://effyai.effybiz.com/temp/', 'home/e']}, 
#  'stand': {'ids': [2729222222, 2983648, 291122111], 'dirs': ['home/c']}, 'bus': {'ids': [2729222222, 2983648, 291122111], 'dirs': ['home/c']}}
