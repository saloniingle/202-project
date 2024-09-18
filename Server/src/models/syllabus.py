from src.models.db import db
from src.models.courses import Courses

class Syllabus(db.Model):
    SyllabusID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(Courses.id), nullable=False)
    Content = db.Column(db.Text, nullable=False)