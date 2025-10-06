from flask import Blueprint
from app.views.upload_video_view import VideoUploadView
from app.views.analyze_video import AnalyzeVideoView
from app.views.video_status import VideoStatusView
from app.views.video_summary import VideoSummarizeView
from app.views.serach_video import VideoSearchView
from app.views.open_ended_analysis import OpenEndedAnalysis
from app.views.get_video_files import GetVideoView, ListVideosView, DownloadVideoView

main_bp = Blueprint('main', __name__)

#video upload
video_upload = VideoUploadView.as_view('file-upload')
main_bp.add_url_rule('/upload-file/', view_func=video_upload, methods=['GET', 'POST'])



analyze_video = AnalyzeVideoView.as_view('analyze')
main_bp.add_url_rule('/analyze/', view_func=analyze_video, methods=['GET'])

video_status = VideoStatusView.as_view('video-status')
main_bp.add_url_rule('/video-status/', view_func=video_status, methods=['GET'])

video_summary = VideoSummarizeView.as_view('video-summary')
main_bp.add_url_rule('/video-summarize/', view_func=video_summary, methods=['GET'])

video_search = VideoSearchView.as_view('search-video')
main_bp.add_url_rule('/search-video/', view_func=video_search, methods=['GET'])

main_bp.add_url_rule('/open-ended-analysis/', view_func=OpenEndedAnalysis.as_view('open-ended-analysis'), methods=['GET'])
main_bp.add_url_rule('/list-videos/', view_func=ListVideosView.as_view('list-videos'), methods=['GET'])
main_bp.add_url_rule('/get-video/', view_func=OpenEndedAnalysis.as_view('get-video'), methods=['GET'])
main_bp.add_url_rule('/download-video/', view_func=DownloadVideoView.as_view('download-video'), methods=['GET'])