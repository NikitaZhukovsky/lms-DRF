from django.contrib import admin
from django.urls import path
from catalog.views import (CourseListView, AddCourseView, CourseView, ModuleListView, AddCourseModuleView,
                           CourseModuleView, LessonListView, AddLessonView, LessonView)

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('add-course/', AddCourseView.as_view(), name='add_course'),
    path('course/<int:course_id>/', CourseView.as_view(), name='course'),
    path('modules/', ModuleListView.as_view(), name='modules'),
    path('add-module/', AddCourseModuleView.as_view(), name='add_module'),
    path('module/<int:module_id>/', CourseModuleView.as_view(), name='module'),
    path('lessons/', LessonListView.as_view(), name='lessons'),
    path('add-lesson/', AddLessonView.as_view(), name='add_lesson'),
    path('lesson/<int:lesson_id>/', LessonView.as_view(), name='lesson')
]
