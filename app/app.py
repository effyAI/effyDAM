# Main api - includes api for search and adding new file with tags 
from flask import Flask, request  
from search import search
from base_process import new_data
import datetime

app = Flask(__name__)

# gunicorn -w 4 -b 0.0.0.0:8000 app:app --timeout 99999999

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
    print("Successfully completed.")
    return output
    # input: id,uid,s3_url, dir, type


if __name__ == "__main__":
    app.run(port= 8000)