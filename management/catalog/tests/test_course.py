import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import Course


@pytest.mark.django_db
def test_create_course_as_admin():
    User = get_user_model()
    User.objects.all().delete()
    Course.objects.all().delete()
    admin_user = User.objects.create_superuser(
        email='admin@example.com',
        password='adminpassword',
    )

    client = APIClient()
    client.force_authenticate(user=admin_user)

    course_data = {
        'title': 'Test Course',
        'description': 'This is a tests course',
        'format': 'Online',
        'date_start': date.today(),
        'date_end': date.today(),
        'teacher': admin_user.id,
    }

    create_course_url = reverse('courses')
    response = client.post(create_course_url, data=course_data)

    assert response.status_code == 200
    assert Course.objects.filter(title='Test Course').exists()
