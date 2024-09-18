from src.models.db import db
from src.models.studentsEnrollment import StudentsEnrollment
from src.models.quizzes import Quizzes

class QuizGrades(db.Model):
    __tablename__ = 'quiz_grades'

    GradeID = db.Column(db.Integer, primary_key=True)
    EnrollmentID = db.Column(db.Integer, db.ForeignKey(StudentsEnrollment.EnrollmentID), nullable=False)
    Grade = db.Column(db.Integer, nullable=False)
    QuizID = db.Column(db.Integer, db.ForeignKey(Quizzes.QuizID), nullable=False)