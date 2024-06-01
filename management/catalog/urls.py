from django.contrib import admin
from django.urls import path
from catalog.views import CourseListView, CourseView, CourseUpdateView

urlpatterns = [
    path('courses/', CourseListView.as_view(), name='courses'),
    path('course/', CourseView.as_view(), name='add_course'),
    path('course/<int:course_id>/', CourseUpdateView.as_view(), name='update_course')
]