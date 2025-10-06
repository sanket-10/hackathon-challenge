from app.db import db
from datetime import datetime

# class Indexes(db.Model):
#     __tablename__ = 'indexes'  # Optional: specify table name
#
#     index_id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#
#     # Optional: backref to videos
#     videos = db.relationship('Videos', backref='index', lazy=True)
#
#     def __repr__(self):
#         return f"<Indexes {self.title}>"



class Videos(db.Model):
    __tablename__ = 'videos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    video_id = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return self.title
