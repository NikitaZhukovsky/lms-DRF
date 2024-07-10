from rest_framework import permissions
from catalog.models import Course, StudentCourse, CourseModule, Lesson, LessonContent
from rest_framework.exceptions import PermissionDenied


class HasLessonAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        else:
            lesson_id = view.kwargs.get('lesson_id')
            try:
                lesson = Lesson.objects.get(pk=lesson_id)
            except Lesson.DoesNotExist:
                raise PermissionDenied('Lesson does not exist')
            module = lesson.module
            course = module.course

            return StudentCourse.objects.filter(student=user, course=course).exists() and \
                   CourseModule.objects.filter(id=module.id, course=course).exists()


class HasLessonContentAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff or user.role == 'Teacher':
            return True
        else:
            lesson_content_id = view.kwargs.get('pk')
            try:
                lesson_content = LessonContent.objects.get(pk=lesson_content_id)
            except LessonContent.DoesNotExist:
                raise PermissionDenied('Lesson content does not exist')
            lesson = lesson_content.lesson
            module = lesson.module
            course = module.course

            return StudentCourse.objects.filter(student=user, course=course).exists()
