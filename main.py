#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__) #to start Flask app
api = Api(app) #to initialize restful API

videos = {}

class Video(Resource):
    def get(self,video_id):
        return videos[video_id]

    def put(self,video_id):
        print(request.form)
        return {}

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
