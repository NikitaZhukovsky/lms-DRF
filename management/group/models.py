from django.db import models
from catalog.models import Course, Lesson
from users.models import CustomUser


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)


class StudentGroup(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False, blank=False)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)


class StudentLesson(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=False, blank=False)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    mark = models.IntegerField(null=True, blank=True)
    attendance = models.BooleanField(null=False, blank=False)


