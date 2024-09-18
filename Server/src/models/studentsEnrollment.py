from src.models.db import db
from src.models.users import User
from src.models.courses import Courses

class StudentsEnrollment(db.Model):
    EnrollmentID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    CourseID = db.Column(db.Integer, db.ForeignKey(Courses.id), nullable=False)