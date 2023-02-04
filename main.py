from flask import Flask
from flask_restful import Api, Resource, reqparse, abort

app = Flask(__name__)
api = Api(app)

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=str, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=str, help="Likes of the video", required=True)

videos = {}

def abort_if_id_not_exist(id: 'id of the object', storage: 'object location') -> 'checker':
    if id not in storage:
        abort(404, message="Id is not valid...")

class Video(Resource):

    def get(self, video_id):
        abort_if_id_not_exist(video_id, videos)
        return videos[video_id]

    def put(self, video_id):
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201

api.add_resource(Video, "/video/<int:video_id>") #(classname, url)

if __name__ == "__main__":
    app.run(debug=True)