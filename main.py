from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

if __name__ == "__main__":
#running debug=True because we are in a production env
    app.run(debug=True)
