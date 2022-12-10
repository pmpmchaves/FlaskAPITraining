#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

import requests

BASE = "http://127.0.0.1:5000/"

data = [{"likes":89, "name": "Carol", "views":4500},
        {"likes":10, "name": "Manuel", "views":234000},
        {"likes":1000, "name": "Johanna", "views":789000}
        ]

for i in range(len(data)):
    response = requests.put(BASE + "video/" + str(i), data[i])
    print(response.json())

response = requests.delete(BASE + "video/0")
print(response)
input()
response = requests.get(BASE + "video/2")
print(response.json())
