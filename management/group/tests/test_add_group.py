import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import date
from catalog.models import Course
from group.models import Group


@pytest.mark.django_db
def test_create_group():
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

    client = APIClient()
    client.force_authenticate(user=admin_user)

    group_data = {
        'course': course.id,
        'name': 'Test Group',
    }

    create_group_url = reverse('group-list')
    response = client.post(create_group_url, data=group_data)

    assert response.status_code == 201
    assert Group.objects.filter(course=course, name='Test Group').exists()
