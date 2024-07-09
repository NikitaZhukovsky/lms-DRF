from celery import shared_task
from catalog.models import StudentCourse, CourseModule, LessonContent, Lesson, Course
from django.core.mail import send_mail
from django.conf import settings


@shared_task()
def update_course_notif(student_id, course_id):
    student_course = StudentCourse.objects.filter(student_id=student_id, course_id=course_id).first()

    if student_course:
        send_mail(
            'Вы подключены к новому курсу',
            f'Здравствуйте, {student_course.student.first_name}! '
            f'Вы были подключены к новому курсу "{student_course.course.title}".',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student_course.student.email],
        )


@shared_task()
def delete_course_notif(student_id, course_id):
    student_course = StudentCourse.objects.filter(student_id=student_id, course_id=course_id).first()

    if student_course:
        send_mail(
            'Вы были удалены из курса',
            f'Здравствуйте, {student_course.student.first_name}! '
            f'Вы были удалены из курса "{student_course.course.title}".',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[student_course.student.email],
        )


@shared_task()
def delete_lesson_content(lesson_id):
    lesson_content = LessonContent.objects.get(lesson_id=lesson_id)
    lesson = Lesson.objects.get(id=lesson_id)
    course_module = CourseModule.objects.get(id=lesson.module_id)
    course = Course.objects.get(id=course_module.course_id)
    student_courses = StudentCourse.objects.filter(course=course)
    if student_courses:
        for student_course in student_courses:
            send_mail(
                f"Файл {lesson_content.name} был удален",
               f"Здравствуйте, {student_course.student.first_name},"
               f" файл {lesson_content.name} для занятия '{lesson.title}' в модуле '{course_module.title}' был удален.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student_course.student.email]
            )


@shared_task()
def add_lesson_content(lesson_id):
    lesson_content = LessonContent.objects.filter(lesson_id=lesson_id).first()
    lesson = Lesson.objects.get(id=lesson_id)
    course_module = CourseModule.objects.get(id=lesson.module_id)
    course = Course.objects.get(id=course_module.course_id)
    student_courses = StudentCourse.objects.filter(course=course)
    if student_courses:
        for student_course in student_courses:
            send_mail(
                f"Файл {lesson_content.name} был добавлен",
               f"Здравствуйте, {student_course.student.first_name},"
               f" файл {lesson_content.name} для занятия '{lesson.title}' в модуле '{course_module.title}' был добавлен.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[student_course.student.email]
            )




