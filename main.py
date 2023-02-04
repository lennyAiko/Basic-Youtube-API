from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# store in chosen folder 'sqlite:///#/database.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# model to store videos
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    # a wrapper method, a good representation of the object
    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video", required=True)

videos = {}

def abort_if_id_not_exist(id: 'id of the object', storage: 'object location') -> 'checker':
    if id not in storage:
        abort(404, message="ID is not valid...")

def abort_if_id_exists(id: 'id of the object', storage: 'object location') -> 'checker':
    if id in storage:
        abort(409, message="ID already exists...")

class Video(Resource):

    def get(self, video_id):
        abort_if_id_not_exist(video_id, videos)
        return videos[video_id]

    def put(self, video_id):
        abort_if_id_exists(video_id, videos)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201
    
    def delete(self, video_id):
        abort_if_id_not_exist(video_id, videos)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>") #(classname, url)

if __name__ == "__main__":
    app.run(debug=True)