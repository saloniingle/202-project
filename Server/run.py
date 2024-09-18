from sqlalchemy import text

from src.app import app
from src.routes.helloworld import bp1
from src.routes.login import login_bp
from src.routes.courses import courses_bp
from src.routes.logout import logout_bp
from src.routes.faculty import faculty_bp
from src.routes.profile import profile_bp
from src.models.db import db
from src.models.users import User
from src.models.courses import Courses
from src.models.studentsEnrollment import StudentsEnrollment
from src.models.syllabus import Syllabus
from src.models.quizGrades import QuizGrades
from src.models.quizzes import Quizzes
from src.models.assignmentGrades import AssignmentGrades
from src.models.assignments import Assignments

app.register_blueprint(bp1)
app.register_blueprint(login_bp)
app.register_blueprint(courses_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(faculty_bp)
app.register_blueprint(profile_bp)

# Create and initialize SQLAlchemy instance

def check_database_connection():
    try:
        # Attempt to create a session with SQLAlchemy
        db.session.execute(text('SELECT 1'))
        return True, None  # Connection successful
    except Exception as e:
        # Handle connection errors
        error_message = str(e)
        return False, error_message  # Connection failed

if __name__ == "__main__":
    with app.app_context():
        connected, error_message = check_database_connection()
        if connected:
            print("Database connection successful!")
            # Create all tables defined in your models
            db.create_all()
            # Continue with your Flask application setup
            app.run(host="0.0.0.0", port=8080, debug=True)
        else:
            print(f"Database connection failed: {error_message}")
