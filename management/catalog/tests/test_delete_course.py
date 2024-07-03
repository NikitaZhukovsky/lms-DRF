import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import Course


@pytest.mark.django_db
def test_delete_course_as_admin():
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
        teacher=admin_user
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    delete_course_url = reverse('courses_set', args=[course.id])
    response = client.delete(delete_course_url)

    assert response.status_code == 200
    assert not Course.objects.filter(title='Test Course').exists()