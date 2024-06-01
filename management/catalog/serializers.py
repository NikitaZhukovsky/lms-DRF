from rest_framework import serializers
from catalog.models import Course, CourseModule, Lesson, LessonContent


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'format', 'date_start', 'date_end', 'teacher')


class DeleteCourseSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()
