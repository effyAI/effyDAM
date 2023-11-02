# Main api - includes api for search and adding new file with tags 
import flask
from flask import Flask, request  
from search import get_info

app = Flask(__name__)

@app.route("/")
def home():
    return "Home"

@app.route("/search_keyword", methods = ['POST'])
def search_keyword():
    data = request.get_json()


    output = get_info(data=data)
    return {"output":output}

@app.route("/new", methods = ['POST'])
def new():
    data = request.get_json()
    
    # id,uid,s3_url, dir, type, keywords, caption
    
    return {"output":"output"   }

if __name__ == "__main__":
    app.run(debug=True, port= 8000)