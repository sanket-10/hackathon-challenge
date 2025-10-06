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

            return {"video_id": video_id, "status": video_status}
        except Exception as e:
            return {"error": str(e)}