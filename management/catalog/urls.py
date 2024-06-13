from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views import (CourseViewSet, CourseModuleViewSet, LessonViewSet, LessonContentViewSet,
                        StudentCourseViewSet, CourseImageViewSet)

router = DefaultRouter()
router.register(r'lesson-content', LessonContentViewSet, basename='lesson_content')
router.register(r'course-image', CourseImageViewSet, basename='course_image')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'modules', CourseModuleViewSet, basename='module')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentCourseViewSet, basename='student')

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:student_id>/courses/', StudentCourseViewSet.as_view({'get': 'get_student_courses',
                                                                             'delete': 'delete_student_from_course'}),
         name='students')
]
