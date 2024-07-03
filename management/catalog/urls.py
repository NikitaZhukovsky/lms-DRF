from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalog.views.course_views import CourseView, CourseViewSet
from catalog.views.module_views import CourseModuleView, CourseModuleViewSet
from catalog.views.lesson_views import LessonView, LessonViewSet
from catalog.views.student_course_views import StudentCourseView, StudentCourseViewSet
from catalog.views.file_views import LessonContentViewSet, CourseImageViewSet

router = DefaultRouter()
router.register(r'lesson-content', LessonContentViewSet, basename='lesson_content')
router.register(r'course-image', CourseImageViewSet, basename='course_image')


urlpatterns = [
    path('', include(router.urls)),
    path('courses/', CourseView.as_view(), name='courses'),
    path('courses/<int:course_id>/', CourseViewSet.as_view(), name="courses_set"),
    path('modules/', CourseModuleView.as_view(), name='modules'),
    path('modules/<int:module_id>/', CourseModuleViewSet.as_view(), name='modules_set'),
    path('lessons/', LessonView.as_view(), name='lessons'),
    path('lessons/<int:lesson_id>/', LessonViewSet.as_view(), name='lessons_set'),
    path('students/', StudentCourseView.as_view(), name="students"),
    path('students/<int:student_course_id>/', StudentCourseViewSet.as_view(), name='students_set'),
]
