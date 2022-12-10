#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #to start Flask app
api = Api(app) #to initialize restful API
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db' #define the location of our database
db = SQLAlchemy(app) #to connect databse to app

#Creating the database model (database columns and elements)
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name={name}, views={views}, likes={likes})"

#db.create_all() #to create the database, only do it once! That's why it was commented out...

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help= "Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help= "Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help= "Likes of the video is required", required=True)

videos = {}

#method to inform the user that video_id does not exist
def abort_if_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message = "Could not find video...")

#method to inform the user that video_id already exists
def abort_if_video_already_exists(video_id):
    if video_id in videos:
        abort(409, message = "The video ID you typed already exists...")


class Video(Resource):
    #method to get video information
    def get(self, video_id):
        abort_if_id_doesnt_exist(video_id)
        return videos[video_id]

    #method to submit video information
    def put(self, video_id):
        abort_if_video_already_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

    #method to delete an existing video
    def delete(self, video_id):
        abort_if_id_doesnt_exist(video_id)
        del videos[video_id]
        return "", 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
