from celery import shared_task
from group.models import Group, StudentGroup
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


@shared_task()
def update_group_notif(group_id, student_id):
    student_group = StudentGroup.objects.get(
        Q(group_id=group_id) &
        Q(student_id=student_id)
    )
    group = student_group.group
    student = student_group.student
    send_mail(
        'Вы добавлены в группу',
        f'Здравствуйте, {student.first_name}! '
        f'Вы были добавлены в группу "{group.name}".',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[student.email]
    )


@shared_task()
def delete_group_notif(student_group):
    group = student_group.group
    student = student_group.student
    send_mail(
        'Вы удалены из группы',
        f'Здравствуйте, {student.first_name}! '
        f'Вы были удалены из группы "{group.name}".',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[student.email]
    )
