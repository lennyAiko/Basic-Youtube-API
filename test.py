import requests

BASE = "http://127.0.0.1:5000/"

info = {"likes": 10, "name": "The wild", "views": 120000}

response = requests.put(BASE + "video/1", info)
print(response.json())
input()
response = requests.get(BASE + "video/1")
print(response.json())

# add a URL to increase views and likes



# def abort_if_id_not_exist(id: 'id of the object', storage: 'object location') -> 'checker':
#     if id not in storage:
#         abort(404, message="ID is not valid...")

# def abort_if_id_exists(id: 'id of the object', storage: 'object location') -> 'checker':
#     if id in storage:
#         abort(409, message="ID already exists...")