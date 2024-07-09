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

        try:
            Course.objects.get(title=course_name)
            raise serializers.ValidationError(
                f"Course with title '{course_name}' already exists.")
        except Course.DoesNotExist:
            return data

    def create(self, validated_data):
        return Course.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = ('id', 'title', 'description', 'course')

    def validate(self, data):
        module_title = data.get('title')
        course = data.get('course')

        try:
            module = CourseModule.objects.get(title=module_title, course=course)
            if self.instance and module.pk == self.instance.pk:
                return data
            else:
                raise serializers.ValidationError(f"Course module with title '{module_title}' already exists for this course.")
        except CourseModule.DoesNotExist:
            return data

    def create(self, validated_data):
        return CourseModule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'module', 'type', 'description', 'date_time')


class LessonContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonContent
        fields = ('id', 'lesson', 'name', 'file')

    def validate(self, data):
        lesson_id = data.get('lesson')
        name = data.get('name')
        if LessonContent.objects.filter(lesson=lesson_id).exists():
            raise ValidationError(f"Lesson Content is already exists.")
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


