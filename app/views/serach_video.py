from flask import request
from flask.views import MethodView
from app.views.upload_video_view import client

class VideoSearchView(MethodView):

    def get(self):
        try:
            query = request.args.get('query')
            search_pager = client.search.query(
                index_id="68e15d2066ecb2513d7ee8d1", query_text=query, search_options=["visual", "audio"], )
            print("Search results:")
            search_results = []
            for clip in search_pager:
                search_results.append({
                    'video_index_id': clip.video_id,
                    'score': clip.score,
                    'start': clip.start,
                    'end': clip.end,
                    'confidence': clip.confidence,
                })
            return {'status': True, 'search_results':search_results}, 200

        except Exception as e:
            return {'error':str(e)}, 400