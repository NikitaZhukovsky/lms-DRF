from rest_framework import serializers
from catalog.models import Course, CourseModule, Lesson, LessonContent


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'format', 'date_start', 'date_end', 'teacher')


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = ('id', 'course', 'title', 'description')

