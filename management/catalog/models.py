from django.db import models
from users.models import CustomUser


class Course(models.Model):
    FORMATS = (
        ('Offline', 'Offline'),
        ('Online', 'Online')
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    format = models.CharField(choices=FORMATS, max_length=100, default='Offline')
    date_start = models.DateField(null=False, blank=False)
    date_end = models.DateField(null=False, blank=False)
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class CourseImage(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='courses_images/')


class StudentCourse(models.Model):
    """
    m2m table linking students and courses
    """
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return f"{self.student} {self.course}"


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Lesson(models.Model):
    TYPES = (
        ('Lecture', 'Lecture'),
        ('Practical', 'Practical'),
        ('Test', 'Test'),
        ('Teamwork', 'Teamwork'),
        ('Attestation', 'Attestation')
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE)
    type = models.CharField(choices=TYPES, max_length=100, default='Lecture')
    description = models.TextField(null=True, blank=True)
    date_time = models.DateTimeField(null=False, blank=True)

    def __str__(self):
        return f"{self.title}"


class LessonContent(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    file = models.FileField(upload_to='lessons_files/', null=True)
