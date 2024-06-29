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
        return data


class StudentLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentLesson
        fields = ['id', 'lesson', 'student', 'mark', 'attendance']

    def validate(self, data):
        lesson = data['lesson']
        student = data['student']
        try:
            instance = StudentLesson.objects.get(lesson=lesson, student=student)
            # Если запись существует, обновите ее
            for key, value in data.items():
                setattr(instance, key, value)
            return instance
        except StudentLesson.DoesNotExist:
            # Если запись не существует, создайте новую
            return data

    def create(self, validated_data):
        return StudentLesson.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

