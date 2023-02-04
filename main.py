from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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

# can not be run twice because of overwrite
# with app.app_context():
#     db.create_all()

# for request arguments
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name of the video is required")
video_update_args.add_argument("views", type=int, help="Views of the video")
video_update_args.add_argument("likes", type=int, help="Likes of the video")


resoure_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}

class Video(Resource):

    @marshal_with(resoure_fields) # serializes it with resource_field
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that ID...")
        return result

    @marshal_with(resoure_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="ID is taken...")
        video = VideoModel(
                    id=video_id, 
                    name=args['name'],
                    views=args['views'],
                    likes=args['likes']
                )
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resoure_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Could not find video with that ID, cannot update...")
        
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        db.session.commit()

        return result

    def delete(self, video_id):
        abort_if_id_not_exist(video_id, videos)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>") #(classname, url)

if __name__ == "__main__":
    app.run(debug=True)