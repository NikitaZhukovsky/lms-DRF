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

    def validate(self, data):
        student = data['student']

        if StudentGroup.objects.filter(student=student).exists():
            raise serializers.ValidationError("You can't add a student to another group")


class StudentLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLesson
        fields = ['id', 'lesson', 'student', 'mark', 'attendance']

    def validate(self, data):
        lesson = data['lesson']
        student = data['student']
        if StudentLesson.objects.filter(lesson=lesson, student=student).exists():
            raise serializers.ValidationError("Such record is already exists.")
        return data

