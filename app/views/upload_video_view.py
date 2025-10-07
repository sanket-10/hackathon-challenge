from flask.views import MethodView
from flask import jsonify, request
import os
from twelvelabs import TwelveLabs
from twelvelabs.tasks import TasksRetrieveResponse
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid
import threading
from app.models import Videos
from app.db import db

load_dotenv()
import logging
import os

# Ensure log directory exists
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Configure logging to file
logging.basicConfig(
    level=logging.INFO,  # Or logging.DEBUG for more details
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, mode='a'),  # Append mode
        logging.StreamHandler()  # Optional: also log to console
    ]
)

logger = logging.getLogger(__name__)

# Video status store (use DB in production)
video_status = {}  # Format: {video_id: {"status": "pending", "task_id": None}}

# TwelveLabs setup
API_KEY = os.getenv("TWELVELABS_API_KEY")  # Add this to your .env
INDEX_ID = os.getenv("TWELVELABS_INDEX_ID")  # Add this to your .env
client = TwelveLabs(api_key=API_KEY)

# Set the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), ".." , 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed extensions (optional)
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Background thread function
def process_video_in_background(id):
    try:
        from app import app  # ✅ Lazy import to avoid circular import

        with app.app_context():
            video = Videos.query.get(id)
            if not video:
                logger.warning(f"Video with ID {id} not found.")
                return None
            video.status = "uploading"
            db.session.commit()
            filepath = os.path.join(UPLOAD_FOLDER, video.filepath)
            logger.info(f"Uploading video: {filepath}")

            with open(filepath, "rb") as video_stream:
                task = client.tasks.create(index_id=INDEX_ID, video_file=video_stream)

            def on_task_update(task: TasksRetrieveResponse):
                print(f"[{video.id}] Status: {task.status}")
                logger.info(f"[{video.id}] Task status update: {task.status}")

            task = client.tasks.wait_for_done(task_id=task.id, sleep_interval=5, callback=on_task_update)

            if task.status == "ready":
                video.status = "ready"
                video.video_id = task.video_id
                db.session.commit()
                logger.info(f"Video {video.id} uploaded and indexed successfully.")
            else:
                video.status = "failed"
                db.session.commit()
                logger.error(f"Video {video.id} upload failed. Task status: {task.status}")
        print("video uploaded successfully")
    except Exception as e:
        print(str(e))
        logger.error(f"Exception occurred while processing video ID {id}")
        logger.error(msg=e, exc_info=True)
        # return Exception(e)

class VideoUploadView(MethodView):

    def get(self):
        return {'status':True, 'message':'upload video'}

    def post(self):
        try:
            if 'video' not in request.files:
                return jsonify({'error': 'No video file in request'}), 400

            file = request.files['video']
            if file.filename == '':
                return jsonify({'error': 'Empty filename'}), 400

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                video_uuid = str(uuid.uuid4())
                save_path = os.path.join(UPLOAD_FOLDER, f"{video_uuid}_{filename}")
                file.save(save_path)

                video = Videos(
                    title=filename,
                    filepath=f"{video_uuid}_{filename}",
                    status='pending',
                    # video_index_id=some_id  # <- Add this if it's required
                )

                db.session.add(video)
                db.session.commit()  # Ensure video.id is set and visible to thread

                threading.Thread(target=process_video_in_background, args=(video.id,)).start()

                return jsonify({
                    "message": "Video uploaded successfully.",
                    "video_id": video.id,
                    "status": "pending"
                }), 201
            logger.warning("Unsupported file type uploaded.")
            return jsonify({'error': 'Unsupported file type'}), 400

        except Exception as e:
            logger.exception("Exception occurred during video upload.")
            return jsonify({'error': str(e)}), 500

