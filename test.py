import requests

BASE = "http://127.0.0.1:5000/"

# Test put request to add data in the VideoModel database

data = [{"likes":89, "name": "Carol", "views":4500},
        {"likes":10, "name": "Manuel", "views":234000},
        {"likes":1000, "name": "Johanna", "views":789000}]
for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

input()

# Test get request to get data from the VideoModel database
response = requests.get(BASE + "video/1")
print(response.json())

input()

# Test patch request to update data in the VideoModel database
response = requests.patch(BASE + "video/1", {"likes":40000, "views":500000})
print(response.json())
