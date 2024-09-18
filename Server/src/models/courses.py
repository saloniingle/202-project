from src.models.db import db
from src.models.users import User


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    facultyID = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    publishedStatus = db.Column(db.String(20), nullable=False)
