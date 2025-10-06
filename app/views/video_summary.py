from flask import request
from flask.views import MethodView
from app.views.upload_video_view import client



class VideoSummarizeView(MethodView):

    def get(self):
        try:
            video_id = request.args.get('video_index_id')
            res_summary = client.summarize(
                video_id=video_id,
                type="summary",
                # prompt="<YOUR_PROMPT>",
                # temperature= 0.2
                )

            return {'status':True, 'summary': res_summary.summary}
        except Exception as e:
            return {'error':str(e)}