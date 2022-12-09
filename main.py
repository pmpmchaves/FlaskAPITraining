#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__) #to start Flask app
api = Api(app) #to initialize restful API

class HelloWorld(Resource):
    def get(self):
        return {"data":"Hello World"}

api.add_resource(HelloWorld, "/helloworld")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
