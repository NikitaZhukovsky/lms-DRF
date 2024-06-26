import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import CourseModule, Course


@pytest.mark.django_db
def test_create_course_module_as_admin():
    User = get_user_model()
    User.objects.all().delete()
    Course.objects.all().delete()
    CourseModule.objects.all().delete()
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

    client = APIClient()
    client.force_authenticate(user=admin_user)

    module_data = {
        'title': 'Test Module',
        'description': 'This is a test module',
        'course': course.id,
    }

    create_module_url = reverse('modules')
    response = client.post(create_module_url, data=module_data)

    assert response.status_code == 200
    assert CourseModule.objects.filter(title='Test Module', course=course).exists()