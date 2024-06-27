import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, timedelta
from catalog.models import Course, Lesson, CourseModule

@pytest.mark.django_db
def test_create_lesson_as_admin():
    User = get_user_model()
    User.objects.all().delete()
    Course.objects.all().delete()
    Lesson.objects.all().delete()
    CourseModule.objects.all().delete()

    admin_user = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword',
    )

    course = Course.objects.create(
        title='Test Course',
        description='This is a test course',
        format='Online',
        date_start=datetime.now().date(),
        date_end=datetime.now().date() + timedelta(days=7),
        teacher=admin_user,
    )

    module = CourseModule.objects.create(
        title='Test Module',
        course=course,
        description='This is a test module',
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    lesson_data = {
        'title': 'Test Lesson',
        'description': 'This is a test lesson',
        'type': 'Lecture',
        'date_time': datetime.now().isoformat(),
        'module': module.id,
    }

    create_lesson_url = reverse('lessons')
    response = client.post(create_lesson_url, data=lesson_data, format='json')

    assert response.status_code == 200
    assert Lesson.objects.filter(title='Test Lesson').exists()
    lesson = Lesson.objects.get(title='Test Lesson')
    assert lesson.module == module
    assert lesson.type == 'Lecture'