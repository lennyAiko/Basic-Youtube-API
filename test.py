import requests

BASE = "http://127.0.0.1:5000/"

info = {"likes": 10, "name": "The wild", "views": 120000}

response = requests.put(BASE + "video/1", info)
print(response.json())
input()
response = requests.get(BASE + "video/1")
print(response.json())

# add a URL to increase views and likes