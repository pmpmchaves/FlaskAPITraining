#Personal note: when running this file on VSCode: <folder_path_to_conda_env>/python + <python_file_path>/<file_name>.py

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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

resource_fields = {
                    "id":fields.Integer,
                    "name":fields.String,
                    "views":fields.Integer,
                    "likes":fields.Integer
                } #this dictionary defines the fields from the VideoModel that we want to return 

class Video(Resource):
    #method to get video information
    @marshal_with(resource_fields) #marshal_with takes the output from return and serializes it in a JSON format according to the resource_fields to make sure what we return is a serialized object and can be read by the get request
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() #to search for the required video using its video_id on the VideoModel database. It searches and returns the first instance it finds.
        return result

    #method to submit video information
    @marshal_with(resource_fields) #to serialize response
    def put(self, video_id):
        args = video_put_args.parse_args() #dictionary that stores all the values we submit (put request)
        video = VideoModel(id=video_id,name=args["name"],views=args["views"],likes=args["likes"]) #this creates a new instance of the VideoModel class, i.e. adds new information to our database
        db.session.add(video) #temporarily adding the created video into the database
        db.session.commit() #permanently adding the created video into the database. Similar to GIT, "video" does not go inside the commit command
        return video, 201

    #method to delete an existing video
    def delete(self, video_id):
        del videos[video_id]
        return "", 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
