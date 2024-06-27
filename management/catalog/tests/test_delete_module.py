import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import CourseModule, Course


@pytest.mark.django_db
def test_delete_course_module_as_admin():
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
        description='This is a test module',
        course=course,
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    delete_module_url = reverse('modules_set', args=[module.id])
    response = client.delete(delete_module_url)

    assert response.status_code == 200
    assert not CourseModule.objects.filter(title='Test Module', course=course).exists()