import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import Course, Lesson, CourseModule


@pytest.mark.django_db
def test_delete_lesson_as_admin():
    User = get_user_model()
    admin_user = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword',
    )

    course = Course.objects.create(
        title='Test Course',
        description='This is a test course',
        format='Online',
        date_start=date.today(),
        date_end=date.today(),
        teacher=admin_user,
    )

    module = CourseModule.objects.create(
        title='Test Module',
        course=course,
        description='This is a test module',
    )

    lesson = Lesson.objects.create(
        title='Test Lesson',
        description='This is a test lesson',
        type='Lecture',
        date_time=date.today(),
        module=module,
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    delete_lesson_url = reverse('lessons_set', args=[lesson.id])
    response = client.delete(delete_lesson_url)

    assert response.status_code == 200
    assert not Lesson.objects.filter(title='Test Lesson').exists()