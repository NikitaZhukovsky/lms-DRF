from rest_framework import serializers
from catalog.models import Course, CourseModule, Lesson, LessonContent, StudentCourse, CourseImage
from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'format', 'date_start', 'date_end', 'teacher')


class CourseModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseModule
        fields = ('id', 'title', 'description', 'course')


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'module', 'type', 'description', 'date_time')


class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'name', 'file')


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ('id', 'student', 'course')


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = ('id', 'course', 'name', 'file')


