from rest_framework import serializers
from catalog.models import Course, CourseModule, Lesson, LessonContent, StudentCourse, CourseImage
from users.models import CustomUser
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, data):
        course_name = data.get('title')
        if Course.objects.filter(title=course_name).exists():
            raise ValidationError(f"Course with name '{course_name}' already exists.")
        return data


class CourseModuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseModule
        fields = ('id', 'title', 'description', 'course')

    def validate(self, data):
        module_title = data.get('title')
        if CourseModule.objects.filter(title=module_title).exists():
            raise ValidationError(f"Course with name '{module_title}' already exists.")
        return data


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'module', 'type', 'description', 'date_time')

    def validate(self, data):
        lesson_title = data.get('title')
        if Lesson.objects.filter(title=lesson_title).exists():
            raise ValidationError(f"Course with name '{lesson_title}' already exists.")
        return data


class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'name', 'file')

    def validate(self, data):
        student_id = data.get('student')
        course_id = data.get('course')
        if StudentCourse.objects.filter(course=course_id, student=student_id).exists():
            raise ValidationError(f"Course with name '{lesson_title}' already exists.")
        return data


class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = ('id', 'student', 'course')

    def validate(self, data):
        student_id = data.get('student')
        course_id = data.get('course')
        if StudentCourse.objects.filter(student=student_id, course=course_id).exists():
            raise ValidationError(f"The relationship between students and the course already exists.")
        return data


class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = ('id', 'course', 'name', 'file')


