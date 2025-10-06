from flask.views import MethodView
# from twelvelabs import TwelveLabs
from app.views.upload_video_view import client
from flask import request


class AnalyzeVideoView(MethodView):

    def get(self):
        try:
            video_id = request.args.get('video_index_id')
            # 1. Gist: get title, topics, hashtags
            gist = client.gist(video_id=video_id, types=["title", "topic", "hashtag"])
            # print(gist)
            response = { 'title': gist.title,
                         "Topics": gist.topics,
                         "Hashtags": gist.hashtags
                        }
            return {'status':True, 'response': response}, 200
        except Exception as e:
            return {'error':str(e)}, 400