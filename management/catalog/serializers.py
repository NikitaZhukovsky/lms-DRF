from rest_framework import serializers
from catalog.models import Course, CourseModule, Lesson, LessonContent
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'format', 'date_start', 'date_end', 'teacher')


class CourseModuleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseModule
        fields = ('id', 'title', 'description', 'course')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'module', 'type', 'description', 'date_time')
