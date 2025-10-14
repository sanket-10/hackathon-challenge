from flask import Flask, send_from_directory
from app.routes import main_bp
from flask_cors import CORS
from flask_migrate import Migrate
from app.views.get_video_files import UPLOAD_FOLDER
from app.db import db
from app.models import Videos


migrate = Migrate()


app = Flask(__name__)

app.register_blueprint(main_bp)
CORS(app=app, supports_credentials=True)
# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app, db)

# Serve video file by filename
@app.route('/videos/<filename>')
def serve_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/', methods=['GET'])
def index():
    return {'status': True, 'message': 'Index View'}, 200


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)