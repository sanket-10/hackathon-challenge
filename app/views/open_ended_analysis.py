from flask import request
from flask.views import MethodView
from app.views.analyze_video import client


class OpenEndedAnalysis(MethodView):
    def get(self):
        try:
            video_id = request.args.get('video_index_id')
            prompt = request.args.get('prompt')
            res = client.analyze(video_id=video_id, prompt=prompt)
            # print(f"{res.data}")
            return {'status': True, 'result':res.data}
        except Exception as e:
            return {'error': str(e)}