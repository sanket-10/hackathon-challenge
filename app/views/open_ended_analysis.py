from flask import request
from flask.views import MethodView

from app.models import Videos
from app.views.analyze_video import client


class OpenEndedAnalysis(MethodView):
    def get(self):
        try:
            video_id = request.args.get('video_id')
            prompt = request.args.get('prompt')
            video = Videos.query.filter_by(id=video_id).first()
            video_index_id = video.video_id
            print(video_index_id)
            res = client.analyze(video_id=video_index_id, prompt=prompt)
            print(f"{res.data=}")

            return {'status': True, 'result':res.data}
        except Exception as e:
            return {'error': str(e)},400