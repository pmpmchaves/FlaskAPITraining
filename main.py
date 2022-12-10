#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__) #to start Flask app
api = Api(app) #to initialize restful API

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help= "Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help= "Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help= "Likes of the video is required", required=True)

videos = {}

class Video(Resource):
    def get(self,video_id):
        return videos[video_id]

    def put(self,video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
