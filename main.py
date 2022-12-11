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

#db.create_all() #to create the database, only do it once! That's why it was commented out after being run one time...

video_put_args = reqparse.RequestParser() #argument parser to define what the user MUST supply when adding a new video to the database
video_put_args.add_argument("name", type=str, help= "Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help= "Views of the video is required", required=True)
video_put_args.add_argument("likes", type=int, help= "Likes of the video is required", required=True)

video_update_args = reqparse.RequestParser() #argument parser to define what the user CAN supply when changing an existing video_id in the database.
                                            #Here we have required=False since the user may want to change only one element of the video characteristics
                                            #IMPORTANT: The argument parser will fill the video_update_args dictionary with a None value for "name", "views" or "likes" if no data is passed for those elements. Example, if "views" is changed to 20000 but no "name" or "likes" update is given, we get: {"name":None, "views":20000,"likes":None}
video_update_args.add_argument("name", type=str, help= "Name of the video is required", required=False)
video_update_args.add_argument("views", type=int, help= "Views of the video is required", required=False)
video_update_args.add_argument("likes", type=int, help= "Likes of the video is required", required=False)


resource_fields = {
                    "id":fields.Integer,
                    "name":fields.String,
                    "views":fields.Integer,
                    "likes":fields.Integer
                } #It is a dictionary defines the fields from the VideoModel that we want to return 

class Video(Resource):
    #method to get video information
    @marshal_with(resource_fields) #marshal_with takes the output from return and serializes it in a JSON format according to the resource_fields to make sure what we return is a serialized object and can be read by the get request
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first() #to search for the required video using its video_id on the VideoModel database. It searches and returns the first instance it finds.
        
        if not result: #if there is no video_id in the database that matches our get request, we need to prevent the model from crashing
            abort(404, message = "Could not find video with that ID")
        
        return result

    #method to submit video information
    @marshal_with(resource_fields) #to serialize response
    def put(self, video_id):
        args = video_put_args.parse_args() #dictionary that stores all the values we submit (put request)
        result = VideoModel.query.filter_by(id=video_id).first() #to check if the video_id we want to add/put to the database already exists. If it does, we need to make sure the code does not break
        if result: #if the video_id already exists, we will display an error message using abort method. This way, the code does not break
            abort(409, message ="Video ID taken...") 
        
        video = VideoModel(id=video_id,name=args["name"],views=args["views"],likes=args["likes"]) #this creates a new instance of the VideoModel class, i.e. adds new information to our database
        db.session.add(video) #temporarily adding the created video into the database
        db.session.commit() #permanently adding the created video into the database. Similar to GIT, "video" does not go inside the commit command
        
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id): #method to update an element (e.g. views, likes) of a given video
        args = video_update_args.parse_args() #we use the update arguments passed by the user
        result = VideoModel.query.filter_by(id=video_id).first() #first we check if the video exists in the database
        if not result: #if the video_ID does not exist in the database, we abort
            abort(404, message = "Video does not exist, cannot update...")

        if args["name"]: #When we write if args["name"], we are testing if the element inside the video_update_args parser dictionary is NOT None. Look at the IMPORTANT note written on the video_update_args parser in line 31 to understand better.
            result.name = args["name"] #if the video does exist, we check which elements were requested to be changed in the database for that video_id and update that database instance with the new values
        if args["likes"]:                
            result.likes = args["likes"]
        if args["views"]:
            result.views = args["views"]

        db.session.commit() #No need to type db.session.add() since the changes are automatically temporarily updated in the database. However, we do need to commit those changes to make them permanent
        
        return result


    #method to delete an existing video
    def delete(self, video_id):
        del videos[video_id]
        return "", 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
