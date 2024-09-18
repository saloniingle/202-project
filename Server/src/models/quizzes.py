from src.models.db import db
from src.models.courses import Courses

class Quizzes(db.Model):
    QuizID = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, db.ForeignKey(Courses.id), nullable=False)
    Title = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.Text, nullable=True)
    MaxGrade = db.Column(db.Integer, nullable=False)