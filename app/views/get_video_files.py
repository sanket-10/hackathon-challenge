from flask import Flask, send_from_directory, jsonify, url_for, request
import os
from app.models import Videos
from flask.views import MethodView

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class GetVideoView(MethodView):
    def get(self):
        filename = request.args.get('filename')
        return send_from_directory(UPLOAD_FOLDER, filename)




class ListVideosView(MethodView):
    def get(self):
        try:
            videos = Videos.query.all()

            videos_list = []
            for video in videos:
                videos_list.append({'video_id': video.id,
                                    'status': video.status,
                                    'title': video.title,
                                    'date_uploaded': video.created_at,
                                    })
            return {'status': True, 'videos_list': videos_list}, 200
        except Exception as e:
            return {'error': str(e)}, 400


from flask import send_from_directory, abort
from app.views.upload_video_view import UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class DownloadVideoView(MethodView):
    def get(self):
        try:
            video_id = request.args.get('video_id')

            video =Videos.query.filter_by(id=video_id).first()

            filepath = video.filepath
            filename = video.title

            # Security check: prevent path traversal
            if not filename.lower().endswith('.mp4'):
                return {'error':"Only MP4 files are allowed."}, 400


            return send_from_directory(UPLOAD_FOLDER, filepath, as_attachment=True, mimetype='video/mp4')

        except Exception as e:
            return {'error': str(e)}, 400
