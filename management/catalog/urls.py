from django.contrib import admin
from django.urls import path
from catalog.views import CourseListView, AddCourseView, CourseView, AddCourseModuleView, CourseModuleView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('course/', AddCourseView.as_view(), name='add_course'),
    path('course/<int:course_id>/', CourseView.as_view(), name='update_course'),
    path('module/', AddCourseModuleView.as_view(), name='add_module'),
    path('module/<int:module_id>/', CourseModuleView.as_view(), name='module')
]