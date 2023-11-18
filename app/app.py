# Main api - includes api for search and adding new file with tags 
from flask import Flask, request  
from search_process import search
from base_process import new_data
import datetime

app = Flask(__name__)

@app.route("/") 
def home():
    return "Home"

# input_data = {"data": ["keyword1","keyword2"] or "man with bike", filter = None or"image" or "video"} -> # output = {"ids":[],"dirs":[] }
@app.route("/search", methods = ['POST']) 
def search_data():
    print("Search request")
    data = request.get_json()
    output = search(data)
    return output


@app.route("/upload", methods = ['POST']) 
def upload():

    print(f"Something got uploaded at {datetime.datetime.now()}")
    data = request.get_json()
    
    output = new_data(data)
    # input: id,uid,s3_url, dir, type


if __name__ == "__main__":
    app.run(port= 8000)