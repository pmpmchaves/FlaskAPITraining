#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

import requests
from requests.auth import HTTPBasicAuth

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "helloworld")

print(response.status_code)
print(response.json())
