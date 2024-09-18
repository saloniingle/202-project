# Features to implement in Client


## **Changes required for Admin Role:**

***In courses page*** --> /courses
- add two dropdown, one for faculty list and other for semester list


***In course page*** --> /courses/:courseID
- here add option to assign course to a faculty for a semester
- add option to show student list enrolled in a course.


## **Changes required for Student Role:**
***In courses page*** --> /courses
- show only published courses


***In course page*** --> /courses/:courseID
- add option to go to announcement, assignments


***In assignments page*** --> /courses/:courseID/assignments
- show list of published assignments and quizzes.


***In profile page*** --> /profile
- add a form to update the username, first name and last name, toggle button for enabling or disabling notification



## **Changes required for Faculty Role:**
***In announcement page*** --> /announcement
- add one input box for heading, one textinput box for body and "Post" button for posting it. 

***In course page*** --> /courses/:courseID
- add option to go to announcement, assignments

***In assignments page*** --> /courses/:courseID/assignments
- show list of published assignments and quizzes.
- show button "Add assignment/quiz"