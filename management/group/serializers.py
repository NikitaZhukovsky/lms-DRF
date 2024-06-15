from rest_framework import serializers
from group.models import Group, StudentGroup, StudentLesson


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'course', 'name']


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentGroup
        fields = ['id', 'group', 'student']


class StudentLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLesson
        fields = ['id', 'lesson', 'student', 'mark', 'attendance']
