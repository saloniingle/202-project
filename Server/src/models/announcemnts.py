from src.models.db import db
from src.models.courses import Courses

class Announcements(db.Model):
    AnnouncementID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(Courses.id), nullable=False)
    AnnouncementText = db.Column(db.Text, nullable=False)
    DatePosted = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)