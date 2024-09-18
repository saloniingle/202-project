from src.models.db import db
from src.models.studentsEnrollment import StudentsEnrollment
from src.models.assignments import Assignments

class AssignmentGrades(db.Model):
    __tablename__ = 'assignment_grades'
    
    GradeID = db.Column(db.Integer, primary_key=True)
    EnrollmentID = db.Column(db.Integer, db.ForeignKey(StudentsEnrollment.EnrollmentID), nullable=False)
    Grade = db.Column(db.Integer, nullable=False)
    AssignmentID = db.Column(db.Integer, db.ForeignKey(Assignments.AssignmentID), nullable=False)