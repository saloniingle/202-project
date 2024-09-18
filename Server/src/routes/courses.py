from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.sql import or_

from src.models.db import db
from src.models.courses import Courses
from src.models.syllabus import Syllabus
from src.models.studentsEnrollment import StudentsEnrollment
from src.models.users import User
from src.models.quizGrades import QuizGrades
from src.models.quizzes import Quizzes
from src.models.assignments import Assignments
from src.models.assignmentGrades import AssignmentGrades
from src.models.announcemnts import Announcements
from src.services.tokenManager import get_id_from_token, get_role_from_token

from src.constants.errors import ErrorCostants
from src.constants.courses import CourseConstants
from src.constants.roles import RoleConstants
from src.services.loginManager import login_required

courses_bp = Blueprint("Courses", __name__, url_prefix="/courses")


def is_null_or_empty(field):
    if field is None or not str(field).strip():
        return True

    return False


@courses_bp.route("", methods=['POST'])
@login_required(roles=[RoleConstants.ADMIN])
def add_course():
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]

    data = request.get_json()
    name = data.get("name")
    semester = data.get("semester")
    faculty_id = data.get("faculty_id")
    published_status = data.get("published_status")
    year = data.get("year")

    if is_null_or_empty(name):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("name")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(semester):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("semester")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(faculty_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("faculty_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(published_status):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("published_status")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(year):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("year")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    course = Courses.query.filter_by(name=name, semester=semester, year=year, facultyID=faculty_id).first()
    if course is not None and course.publishedStatus != published_status:
        if published_status:
            course.publishedStatus = CourseConstants.PUBLISHED_STATUS
        else:
            course.publishedStatus = CourseConstants.UNPUBLISHED_STATUS
        db.session.add(course)
        db.session.commit()
        db.session.refresh(course)
        return jsonify({"message": f"Successfully updated the course with id: {course.id}"})
    elif course is not None:
        return jsonify({"error": ErrorCostants.COURSE_ALREADY_EXISTS["message"].format("year")}), ErrorCostants.COURSE_ALREADY_EXISTS["http_status_code"]

    course = Courses()
    course.facultyID = faculty_id
    course.year = year
    if published_status:
        course.publishedStatus = CourseConstants.PUBLISHED_STATUS
    else:
        course.publishedStatus = CourseConstants.UNPUBLISHED_STATUS
    course.name = name
    course.semester = semester

    db.session.add(course)
    db.session.commit()
    db.session.refresh(course)

    syllabus = Syllabus()
    syllabus.CourseID = course.id
    syllabus.Content = ""

    db.session.add(syllabus)
    db.session.commit()
    db.session.refresh(syllabus)

    return jsonify({"message": f"Successfully added the course with id: {course.id}"})


@courses_bp.route("/<course_id>/syllabus", methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def update_syllabus(course_id):
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]
    
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]

    data = request.get_json()
    syllabus_content = data.get("syllabusContent")

    if is_null_or_empty(syllabus_content):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("syllabusContent")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        syllabus = Syllabus.query.filter_by(CourseID=course_id).first()
        if syllabus is None:
            return jsonify({"error": "Invalid Course!"}), 400
        
        syllabus.Content = syllabus_content

        db.session.add(syllabus)
        db.session.commit()
        db.session.refresh(syllabus)

        syllabus_json = {
            'SyllabusID': syllabus.SyllabusID,
            'CourseID': syllabus.CourseID,
            'Content': syllabus.Content
        }

        return jsonify(syllabus_json)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

def get_student_list(course_id):
    enrollment_list = StudentsEnrollment.query.filter_by(CourseID=course_id).all()

    student_list = []
    for enrollment in enrollment_list:
        student = User.query.filter_by(id=enrollment.UserID).first()
        if student is not None:
            student_info = {
                'id': student.id,
                'enrollment_id': enrollment.EnrollmentID,
                'username': student.username,
                'first_name': student.first_name,
                'last_name': student.last_name
            }
            student_list.append(student_info)
    
    return student_list

@courses_bp.route("/<course_id>/students", methods=['GET'])
@login_required(roles=[RoleConstants.FACULTY, RoleConstants.ADMIN])
def get_student_list_for_course(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)

    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    role = get_role_from_token(token=token)

    try:
        if role.lower() == RoleConstants.FACULTY:
            course = Courses.query.filter_by(id=course_id, facultyID=user_id).first()
            if course is None :
                return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
            return jsonify(get_student_list(course_id=course_id))

        return jsonify(get_student_list(course_id=course_id))
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]


@courses_bp.route("/get_quiz_grades", methods=['GET'])
@login_required(roles=["faculty"])
def get_quiz_grades():
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]
    
    data = request.get_json()
    quiz_id = data.get("quiz_id")
    enrollment_id = data.get("enrollment_id")

    if is_null_or_empty(quiz_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("quiz_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(enrollment_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("enrollment_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        quiz_grades = QuizGrades.query.filter_by(QuizID=quiz_id, EnrollmentID=enrollment_id).first()
        if not quiz_grades:
            return jsonify({"error": "No grades available!"}), 400
        quiz_grades_info = {
            'GradeID': quiz_grades.GradeID,
            'EnrollmentID': quiz_grades.EnrollmentID,
            'Grade': quiz_grades.Grade,
            'QuizID': quiz_grades.QuizID
        }
        return jsonify(quiz_grades_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    

@courses_bp.route("/get_assignment_grades", methods=['GET'])
@login_required(roles=["faculty"])
def get_assignment_grades():
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]
    
    data = request.get_json()
    assignment_id = data.get("assignment_id")
    enrollment_id = data.get("enrollment_id")

    if is_null_or_empty(assignment_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("assignment_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(enrollment_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("enrollment_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        assignment_grades = AssignmentGrades.query.filter_by(AssignmentID=assignment_id, EnrollmentID=enrollment_id).first()
        if not assignment_grades:
            return jsonify({"error": "No grades available!"}), 400
        assignment_grades_info = {
            'GradeID': assignment_grades.GradeID,
            'EnrollmentID': assignment_grades.EnrollmentID,
            'Grade': assignment_grades.Grade,
            'AssignmentID': assignment_grades.AssignmentID
        }
        return jsonify(assignment_grades_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    

@courses_bp.route("/<course_id>/quiz/<quiz_id>/grades", methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def assign_quiz_grades(course_id, quiz_id):
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]
    
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    quiz = Quizzes.query.filter_by(QuizID=quiz_id, CourseID=course_id).first()
    if quiz is None:
        return jsonify({"error": ErrorCostants.QUIZ_NOT_FOUND["message"].format(quiz_id)}), ErrorCostants.QUIZ_NOT_FOUND["http_status_code"]
    
    data = request.get_json()
    enrollment_id = data.get("enrollment_id")
    student_grades = data.get("student_grades")
    
    if quiz.MaxGrade < int(student_grades) or student_grades < 0:
        return jsonify({"error": ErrorCostants.INVALID_MARKS_FOUND["message"].format(quiz.MaxGrade)}), ErrorCostants.INVALID_MARKS_FOUND["http_status_code"]

    if is_null_or_empty(enrollment_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("enrollment_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(student_grades):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("student_grades")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        quiz_grades = QuizGrades.query.filter_by(QuizID=quiz_id, EnrollmentID=enrollment_id).first()
        if quiz_grades is None:
            quiz_grades = QuizGrades()
        
        quiz_grades.EnrollmentID = enrollment_id
        quiz_grades.Grade = student_grades
        quiz_grades.QuizID = quiz_id

        db.session.add(quiz_grades)
        db.session.commit()
        db.session.refresh(quiz_grades)

        quiz_grades_info = {
            'GradeID': quiz_grades.GradeID,
            'EnrollmentID': quiz_grades.EnrollmentID,
            'Grade': quiz_grades.Grade,
            'QuizID': quiz_grades.QuizID
        }
        return jsonify(quiz_grades_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    

@courses_bp.route("/<course_id>/assignment/<assignment_id>/grades", methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def assign_assignment_grades(course_id, assignment_id):
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]
    
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    assignment = Assignments.query.filter_by(AssignmentID=assignment_id, CourseID=course_id).first()
    if assignment is None:
        return jsonify({"error": ErrorCostants.AASSIGNMENT_NOT_FOUND["message"].format(assignment_id)}), ErrorCostants.AASSIGNMENT_NOT_FOUND["http_status_code"]

    data = request.get_json()
    enrollment_id = data.get("enrollment_id")
    student_grades = data.get("student_grades")

    if assignment.MaxGrade < int(student_grades) or student_grades < 0:
        return jsonify({"error": ErrorCostants.INVALID_MARKS_FOUND["message"].format(assignment.MaxGrade)}), ErrorCostants.INVALID_MARKS_FOUND["http_status_code"]

    if is_null_or_empty(enrollment_id):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("enrollment_id")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(student_grades):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("student_grades")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        assignment_grades = AssignmentGrades.query.filter_by(AssignmentID=assignment_id, EnrollmentID=enrollment_id).first()
        if assignment_grades is None:
            assignment_grades = AssignmentGrades()

        assignment_grades.EnrollmentID = enrollment_id
        assignment_grades.Grade = student_grades
        assignment_grades.AssignmentID = assignment_id

        db.session.add(assignment_grades)
        db.session.commit()
        db.session.refresh(assignment_grades)

        assignment_grades_info = {
            'GradeID': assignment_grades.GradeID,
            'EnrollmentID': assignment_grades.EnrollmentID,
            'Grade': assignment_grades.Grade,
            'AssignmentID': assignment_grades.AssignmentID
        }
        return jsonify(assignment_grades_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
@courses_bp.route('/<course_id>/announcements', methods=['GET'])
@login_required(roles=[RoleConstants.STUDENT, RoleConstants.FACULTY])
def get_announcements(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token=token)

    if role.lower() == RoleConstants.FACULTY:
        is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
        if not is_faculty_authorized:
            return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    if role.lower() == RoleConstants.STUDENT:
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.USER_NOT_AUTHORIZED["message"]}), ErrorCostants.USER_NOT_AUTHORIZED["http_status_code"]
    
    announcements = Announcements.query.filter_by(CourseID=course_id).all()
    announcement_json = []
    for announcement in announcements:
        announcement_info = {
            'announcementID': announcement.AnnouncementID,
            'courseID': announcement.CourseID,
            'announcementText': announcement.AnnouncementText,
            'datePosted': announcement.DatePosted
        }
        announcement_json.append(announcement_info)
    return jsonify(announcement_json)

@courses_bp.route('/<course_id>/announcement', methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def create_announcement(course_id):
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]

    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]

    data = request.json
    announcement_text = data.get('announcementText')

    if is_null_or_empty(announcement_text):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("announcementText")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        announcement = Announcements(CourseID=course_id, AnnouncementText=announcement_text)
        db.session.add(announcement)
        db.session.commit()
        db.session.refresh(announcement)

        announcement_info = {
            "announcementID": announcement.AnnouncementID,
            "courseID": announcement.CourseID,
            "announcementText": announcement.AnnouncementText,
            "datePosted": announcement.DatePosted
        }
        return jsonify(announcement_info)

    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

@courses_bp.route("/<course_id>/quizzes", methods=['GET'])
@login_required(roles=[RoleConstants.STUDENT, RoleConstants.FACULTY])
def get_quizzes(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token)

    if role.upper() == RoleConstants.STUDENT.upper():
        is_student_enrolled = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_enrolled:
            return jsonify({"error": ErrorCostants.STUDENT_NOT_ENROLLED["message"]}), ErrorCostants.STUDENT_NOT_ENROLLED["http_status_code"]

        quizzes = db.session.query(
            Quizzes
        ).filter(
            Quizzes.CourseID == course_id,
        ).all()

        quizzes_json = []
        for quiz in quizzes:

            quiz_json = {
                "id": quiz.QuizID,
                "title": quiz.Title
            }

            quizzes_json.append(quiz_json)

        return jsonify(quizzes_json)

    else:
        quizzes = db.session.query(Quizzes).filter(Quizzes.CourseID == course_id).all()

        quizzes_json = []
        for quiz in quizzes:

            quiz_json = {
                "id": quiz.QuizID,
                "title": quiz.Title
            }

            quizzes_json.append(quiz_json)

        return jsonify(quizzes_json)


@courses_bp.route("/<course_id>/assignments", methods=['GET'])
@login_required(roles=[RoleConstants.STUDENT, RoleConstants.FACULTY])
def get_assignments(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token)

    if role.upper() == RoleConstants.STUDENT.upper():
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.STUDENT_NOT_ENROLLED["message"]}), ErrorCostants.STUDENT_NOT_ENROLLED

        assignment_details = db.session.query(
            Assignments
        ).filter(
            Assignments.CourseID == course_id,
        ).all()

        assignments_json = []
        for assignment in assignment_details:
            assignment_json = {
                "id": assignment.AssignmentID,
                "title": assignment.Title,
            }

            assignments_json.append(assignment_json)
    else:
        assignments = db.session.query(Assignments).filter(Assignments.CourseID == course_id).all()

        assignments_json = []
        for assignment in assignments:

            assignment_json = {
                "id": assignment.AssignmentID,
                "title": assignment.Title,
            }

            assignments_json.append(assignment_json)

    return jsonify(assignments_json)


def get_faculty_courses(user_id):
    is_published = None
    year = None
    semester = None
    is_published = request.args.get("isPublished")
    if is_published:
        if is_published.lower() == "false":
            is_published = False
        else:
            is_published = True

    year = request.args.get("year")
    semester = request.args.get("semester")

    query = Courses.query.filter(Courses.facultyID == user_id).order_by(Courses.year.desc())
    if is_published:
        query = query.filter(func.lower(Courses.publishedStatus) == func.lower(CourseConstants.PUBLISHED_STATUS))
    elif is_published is not None:
        query = query.filter(func.lower(Courses.publishedStatus) != func.lower(CourseConstants.PUBLISHED_STATUS))

    if year:
        query = query.filter(Courses.year == year)

    if semester:
        query = query.filter(Courses.semester == semester)

    courses = query.all()
    courses_json = []
    for course in courses:
        courses_json.append(
            {
                "courseID": course.id,
                "name": course.name,
                "semester": course.semester,
                "year": course.year,
                "facultyID": course.facultyID,
                "isPublished": course.publishedStatus.lower() == CourseConstants.PUBLISHED_STATUS.lower()
            }
        )

    return courses_json


def get_student_courses(user_id):
    year = None
    semester = None
    year = request.args.get("year")
    semester = request.args.get("semester")

    query = Courses.query.join(StudentsEnrollment).filter(
        Courses.publishedStatus == CourseConstants.PUBLISHED_STATUS
    ).filter(
        StudentsEnrollment.UserID == user_id
    ).order_by(Courses.year.desc())
    print("user_id", user_id)
    if year:
        query = query.filter(Courses.year == year)

    if semester:
        query = query.filter(Courses.semester == semester)

    courses = query.all()
    courses_json = []
    for course in courses:
        courses_json.append(
            {
                "courseID": course.id,
                "name": course.name,
                "semester": course.semester,
                "year": course.year,
                "facultyID": course.facultyID,
                "isPublished": course.publishedStatus.lower() == CourseConstants.PUBLISHED_STATUS.lower()
            }
        )

    return courses_json


def get_admin_courses():
    year = None
    semester = None
    year = request.args.get("year")
    semester = request.args.get("semester")
    facultyID = request.args.get("facultyID")
    is_published = request.args.get("isPublished")
    if is_published:
        if is_published.lower() == "false":
            is_published = False
        else:
            is_published = True

    query = Courses.query
    if year:
        query = query.filter(Courses.year == year)

    if semester:
        query = query.filter(Courses.semester == semester)

    if facultyID:
        query = query.filter(Courses.facultyID == facultyID)

    if is_published:
        query = query.filter(func.lower(Courses.publishedStatus) == func.lower(CourseConstants.PUBLISHED_STATUS))
    elif is_published is not None:
        query = query.filter(func.lower(Courses.publishedStatus) != func.lower(CourseConstants.PUBLISHED_STATUS))

    courses = query.order_by(Courses.year.desc()).all()
    courses_json = []
    for course in courses:
        courses_json.append(
            {
                "courseID": course.id,
                "name": course.name,
                "semester": course.semester,
                "year": course.year,
                "facultyID": course.facultyID,
                "isPublished": course.publishedStatus.lower() == CourseConstants.PUBLISHED_STATUS.lower()
            }
        )

    return courses_json


@courses_bp.route("", methods=['GET'])
@login_required(roles=[RoleConstants.STUDENT, RoleConstants.FACULTY, RoleConstants.ADMIN])
def get_courses():
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token=token)

    try:
        if role.lower() == RoleConstants.FACULTY:
            return jsonify(get_faculty_courses(user_id=user_id))

        elif role.lower() == RoleConstants.STUDENT:
            return jsonify(get_student_courses(user_id=user_id))

        return jsonify(get_admin_courses())

    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]


@courses_bp.route("/<course_id>/assignments", methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def post_assignment(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    data = request.json
    title = data.get('title')
    description = data.get('description')
    maxGrade = data.get('maxGrade')

    if is_null_or_empty(title):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("Title")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(description):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("Description")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(maxGrade):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("MaxGrade")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        assignment = Assignments(CourseID=course_id, Title=title, Description=description, MaxGrade=maxGrade)
        db.session.add(assignment)
        db.session.commit()
        db.session.refresh(assignment)

        assignment_info = {
            'assignmentID': assignment.AssignmentID,
            'courseID': assignment.CourseID,
            'title': assignment.Title,
            'description': assignment.Description,
            'maxGrade': assignment.MaxGrade
        }
        return jsonify(assignment_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

@courses_bp.route("/<course_id>/quizzes", methods=['POST'])
@login_required(roles=[RoleConstants.FACULTY])
def post_quizz(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
    if not is_faculty_authorized:
        return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    data = request.json
    title = data.get('title')
    description = data.get('description')
    maxGrade = data.get('maxGrade')

    if is_null_or_empty(title):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("Title")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(description):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("Description")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    if is_null_or_empty(maxGrade):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("MaxGrade")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]
    
    try:
        quizz = Quizzes(CourseID=course_id, Title=title, Description=description, MaxGrade=maxGrade)
        db.session.add(quizz)
        db.session.commit()
        db.session.refresh(quizz)

        quiz_info = {
            'quizID': quizz.QuizID,
            'courseID': quizz.CourseID,
            'title': quizz.Title,
            'description': quizz.Description,
            'maxGrade': quizz.MaxGrade
        }
        return jsonify(quiz_info)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
      
@courses_bp.route("/", methods=['PUT'])
@login_required(roles=[RoleConstants.ADMIN])
def update_course_faculty():
    if not request.is_json:
        return jsonify({"error": ErrorCostants.JSON_REQUEST_BODY_REQUIRED["message"]}), ErrorCostants.JSON_REQUEST_BODY_REQUIRED["http_status_code"]

    data = request.get_json()
    courseId = data.get("courseId")
    facultyId = data.get("facultyId")

    if is_null_or_empty(courseId):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("courseId")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    if is_null_or_empty(facultyId):
        return jsonify({"error": ErrorCostants.FIELD_CANNOT_BE_EMPTY["message"].format("facultyId")}), ErrorCostants.FIELD_CANNOT_BE_EMPTY["http_status_code"]

    course = Courses.query.filter_by(id=courseId).first()
    if course is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    course.facultyID = facultyId

    db.session.add(course)
    db.session.commit()
    db.session.refresh(course)

    course_info = {
        'id': course.id,
        'name': course.name,
        'semester': course.semester,
        'year': course.year,
        'facultyID': course.facultyID,
        'publishedStatus': course.publishedStatus
    }

    return course_info

@courses_bp.route("/<course_id>/syllabus", methods=['GET'])
@login_required(roles=[RoleConstants.FACULTY, RoleConstants.STUDENT])
def get_syllabus(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]

    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    role = get_role_from_token(token=token)

    if role.lower() == RoleConstants.FACULTY:
        is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
        if not is_faculty_authorized:
            return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    if role.lower() == RoleConstants.STUDENT:
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.STUDENT_NOT_ENROLLED["message"]}), ErrorCostants.STUDENT_NOT_ENROLLED["http_status_code"]

    try:
        syllabus = Syllabus.query.filter_by(CourseID=course_id).first()
        if syllabus is None:
            return jsonify({"error": "Invalid Course!"}), 400

        syllabus_json = {
            'SyllabusID': syllabus.SyllabusID,
            'CourseID': syllabus.CourseID,
            'Content': syllabus.Content
        }

        return jsonify(syllabus_json)
    except Exception as e:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

@courses_bp.route("/<course_id>", methods=['GET'])
@login_required(roles=[RoleConstants.FACULTY, RoleConstants.STUDENT, RoleConstants.ADMIN])
def get_course(course_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token=token)

    if role.lower() == RoleConstants.FACULTY:
        is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
        if not is_faculty_authorized:
            return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
    
    if role.lower() == RoleConstants.STUDENT:
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.STUDENT_NOT_ENROLLED["message"]}), ErrorCostants.STUDENT_NOT_ENROLLED["http_status_code"]
        
    course = Courses.query.filter_by(id=course_id).first()

    course_info = {
        'id': course.id,
        'name': course.name,
        'semester': course.semester,
        'year': course.year,
        'facultyID': course.facultyID,
        'publishedStatus': course.publishedStatus
    }

    return course_info

def get_faculty_assignment(course_id, assignment_id):
    assignment = Assignments.query.filter_by(AssignmentID=assignment_id).first()
    if assignment is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    assignment_json = {
            "assignmentId": assignment.AssignmentID,
            "title": assignment.Title,
            "description": assignment.Description,
            "maxGrade": assignment.MaxGrade,
            "courseId": assignment.CourseID
        }
    
    student_list = get_student_list(course_id)
    studentGradesList = []
    for student in student_list:
        enrollment_id = student['enrollment_id']
        assignment_grades = AssignmentGrades.query.filter_by(AssignmentID=assignment_id,EnrollmentID=enrollment_id).first()
        student_grade_info = {}
        if assignment_grades is not None:
            student_grade_info = {
                'gradeId': assignment_grades.GradeID,
                'enrollmentId': enrollment_id,
                'grade': assignment_grades.Grade,
                'assignmentId': assignment_grades.AssignmentID,
                'maxGrade': assignment.MaxGrade,
                'studentId': student['id'],
                'username': student['username'],
                'firstName': student['first_name'],
                'lastName': student['last_name']
            }
        else:
            student_grade_info = {
                'gradeId': None,
                'enrollmentId': enrollment_id,
                'grade': None,
                'assignmentId': None,
                'maxGrade': assignment.MaxGrade,
                'studentId': student['id'],
                'username': student['username'],
                'firstName': student['first_name'],
                'lastName': student['last_name']
            }
        studentGradesList.append(student_grade_info)
    
    return jsonify({"assignmetInfo": assignment_json, "studentGrades": studentGradesList})

def get_student_assignment(course_id, assignment_id, student_id):
    assignment = Assignments.query.filter_by(AssignmentID=assignment_id).first()
    if assignment is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    assignment_json = {
            "assignmentId": assignment.AssignmentID,
            "title": assignment.Title,
            "description": assignment.Description,
            "maxGrade": assignment.MaxGrade,
            "courseId": assignment.CourseID
        }
    
    enrollment = StudentsEnrollment.query.filter_by(UserID=student_id, CourseID=course_id).first()
    if enrollment is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    enrollment_id = enrollment.EnrollmentID
    assignment_grades = AssignmentGrades.query.filter_by(AssignmentID=assignment_id,EnrollmentID=enrollment_id).first()
    student_grade_info = {}
    if assignment_grades is not None:
        student_grade_info = {
            'gradeId': assignment_grades.GradeID,
            'enrollmentId': enrollment_id,
            'grade': assignment_grades.Grade,
            'assignmentId': assignment_grades.AssignmentID,
            'maxGrade': assignment.MaxGrade
        }
    else:
        student_grade_info = {
            'gradeId': None,
            'enrollmentId': enrollment_id,
            'grade': None,
            'assignmentId': None,
            'maxGrade': assignment.MaxGrade
        }
    
    return jsonify({"assignmetInfo": assignment_json, "studentGrades":student_grade_info})

@courses_bp.route("/<course_id>/assignments/<assignment_id>", methods=['GET'])
@login_required(roles=[RoleConstants.FACULTY, RoleConstants.STUDENT])
def get_assignment(course_id, assignment_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token=token)

    if role.lower() == RoleConstants.FACULTY:
        is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
        if not is_faculty_authorized:
            return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
        return get_faculty_assignment(course_id, assignment_id)
    
    if role.lower() == RoleConstants.STUDENT:
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.USER_NOT_AUTHORIZED["message"]}), ErrorCostants.USER_NOT_AUTHORIZED["http_status_code"]
        return get_student_assignment(course_id, assignment_id, user_id)
    
    return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

def get_faculty_quiz(course_id, quiz_id):
    quiz = Quizzes.query.filter_by(QuizID=quiz_id).first()
    if quiz is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    quiz_json = {
            "quizId": quiz.QuizID,
            "title": quiz.Title,
            "description": quiz.Description,
            "maxGrade": quiz.MaxGrade,
            "courseId": quiz.CourseID
        }
    
    student_list = get_student_list(course_id)
    studentGradesList = []
    for student in student_list:
        enrollment_id = student['enrollment_id']
        quiz_grades = QuizGrades.query.filter_by(QuizID=quiz_id,EnrollmentID=enrollment_id).first()
        student_grade_info = {}
        if quiz_grades is not None:
            student_grade_info = {
                'gradeId': quiz_grades.GradeID,
                'enrollmentId': enrollment_id,
                'grade': quiz_grades.Grade,
                'quizId': quiz_grades.QuizID,
                'maxGrade': quiz.MaxGrade,
                'studentId': student['id'],
                'username': student['username'],
                'firstName': student['first_name'],
                'lastName': student['last_name']
            }
        else:
            student_grade_info = {
                'gradeId': None,
                'enrollmentId': enrollment_id,
                'grade': None,
                'quizId': None,
                'maxGrade': quiz.MaxGrade,
                'studentId': student['id'],
                'username': student['username'],
                'firstName': student['first_name'],
                'lastName': student['last_name']
            }
        studentGradesList.append(student_grade_info)
    
    return jsonify({"quizInfo": quiz_json, "studentGrades": studentGradesList})

def get_student_quiz(course_id, quiz_id, student_id):
    quiz = Quizzes.query.filter_by(QuizID=quiz_id).first()
    if quiz is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    quiz_json = {
            "quizId": quiz.QuizID,
            "title": quiz.Title,
            "description": quiz.Description,
            "maxGrade": quiz.MaxGrade,
            "courseId": quiz.CourseID
        }
    
    enrollment = StudentsEnrollment.query.filter_by(UserID=student_id, CourseID=course_id).first()
    if enrollment is None:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]
    
    enrollment_id = enrollment.EnrollmentID
    quiz_grades = QuizGrades.query.filter_by(QuizID=quiz_id,EnrollmentID=enrollment_id).first()
    student_grade_info = {}
    if quiz_grades is not None:
        student_grade_info = {
            'gradeId': quiz_grades.GradeID,
            'enrollmentId': enrollment_id,
            'grade': quiz_grades.Grade,
            'quizId': quiz_grades.QuizID,
            'maxGrade': quiz.MaxGrade
        }
    else:
        student_grade_info = {
            'gradeId': None,
            'enrollmentId': enrollment_id,
            'grade': None,
            'assignmentId': None,
            'maxGrade': quiz.MaxGrade
        }
    
    return jsonify({"quizInfo": quiz_json, "studentGrades":student_grade_info})


@courses_bp.route("/<course_id>/quizzes/<quiz_id>", methods=['GET'])
@login_required(roles=[RoleConstants.FACULTY, RoleConstants.STUDENT])
def get_quiz(course_id, quiz_id):
    token = None
    if "Authorization" in request.headers:
        token = request.headers["Authorization"].split(" ")[1]
    user_id = get_id_from_token(token)
    if not user_id:
        return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]

    role = get_role_from_token(token=token)

    if role.lower() == RoleConstants.FACULTY:
        is_faculty_authorized = Courses.query.filter_by(facultyID=user_id, id=course_id).first() is not None
        if not is_faculty_authorized:
            return jsonify({"error": ErrorCostants.FACULTY_NOT_AUTHORIZED["message"]}), ErrorCostants.FACULTY_NOT_AUTHORIZED["http_status_code"]
        return get_faculty_quiz(course_id, quiz_id)
    
    if role.lower() == RoleConstants.STUDENT:
        is_student_authorized = StudentsEnrollment.query.filter_by(UserID=user_id, CourseID=course_id).first() is not None
        if not is_student_authorized:
            return jsonify({"error": ErrorCostants.USER_NOT_AUTHORIZED["message"]}), ErrorCostants.USER_NOT_AUTHORIZED["http_status_code"]
        return get_student_quiz(course_id, quiz_id, user_id)
    
    return jsonify({"error": ErrorCostants.SOMETHING_WENT_WRONG["message"]}), ErrorCostants.SOMETHING_WENT_WRONG["http_status_code"]