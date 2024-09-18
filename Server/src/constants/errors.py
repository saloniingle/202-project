class ErrorCostants:
    JSON_REQUEST_BODY_REQUIRED = {"message": "Request body must be in JSON format", "http_status_code": 400}
    FIELD_CANNOT_BE_EMPTY = {"message": "Field `{}` cannot be empty/null", "http_status_code": 400}
    SOMETHING_WENT_WRONG = {"message": "Something went wrong :(", "http_status_code": 400}
    COURSE_NOT_FOUND = {"message": "Course with id: {} not found", "http_status_code": 404}
    STUDENT_NOT_ENROLLED = {"message": "Student is not enrolled in the course", "http_status_code": 400}
    FACULTY_NOT_AUTHORIZED = {"message": "Faculty is not authorized in the course", "http_status_code": 400}
    QUIZ_NOT_FOUND = {"message": "Quiz with id: {} not found", "http_status_code": 404}
    AASSIGNMENT_NOT_FOUND = {"message": "Assignment with id: {} not found", "http_status_code": 404}
    INVALID_MARKS_FOUND = {"message": "Trying to set invalid marks: {}", "http_status_code": 400}
    USER_NOT_AUTHORIZED = {"message": "You are not authorized to see this information", "http_status_code": 400}
    USER_ALREADY_EXISTS = {"message": "Username with username: {} already exists.", "http_status_code": 400}
    COURSE_ALREADY_EXISTS = {"message": "Course is already present", "http_status_code": 400}
