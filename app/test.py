import requests
import time


t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)
for i in range(500):
    data = {
    "uid": i,
    "s3_url": "https://effy-bandhan.s3.amazonaws.com/587f0420-77ab-11ee-9915-5fafeaa0334f.mp4",
    "directory": "home/e",
    "type": "video",
    "date": "",
    "time": ""
    }
    output = requests.post("http://127.0.0.1:8000/upload", json= data)
    print(f"{i} : {output.json()}")

# data = {
#     "uid": 1435,
#     "s3_url": "https://images.pexels.com/photos/5896476/pexels-photo-5896476.jpeg",
#     "directory": "home/e",
#     "type": "image",
#     "date": "",
#     "time": ""
# }

# output = requests.post("http://127.0.0.1:8000/upload", json = data)
# print(f"{1} : {output.json()}")


s = time.localtime()
current_time2 = time.strftime("%H:%M:%S", s)
print(current_time2)