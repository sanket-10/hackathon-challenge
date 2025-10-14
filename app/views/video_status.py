from flask import jsonify, request
from flask.views import MethodView
from app.views.upload_video_view import video_status
from app.models import Videos



# Status API
class VideoStatusView(MethodView):

    def get(self):
        try:
            video_id = request.args.get('video_id')
            video = Videos.query.filter_by(id=video_id).first()
            video_status = video.status
            title = video.title
            date_uploaded = video.created_at#.strftime('%Y-%m-%d %H:%M:%S')

            return {"video_id": video_id, "status": video_status, 'title':title, 'date_uploaded':date_uploaded}, 200
        except Exception as e:
            return {"error": str(e)}, 400