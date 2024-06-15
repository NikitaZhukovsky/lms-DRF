from rest_framework import permissions
from catalog.models import StudentCourse, CourseModule, Lesson, LessonContent
from rest_framework.exceptions import PermissionDenied


class HasModuleAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        else:
            module_id = view.kwargs.get('pk')
            student = user
            try:
                module = CourseModule.objects.get(pk=module_id)
            except CourseModule.DoesNotExist:
                raise PermissionDenied('Module does not exist')

            course = module.course

            return StudentCourse.objects.filter(student=student, course=course).exists()


class HasLessonAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.is_staff:
            return True
        else:
            lesson_id = view.kwargs.get('pk')
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
        if user.is_staff:
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
