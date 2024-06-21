from celery import shared_task
from users.models import CustomUser
from group.models import StudentLesson
from django.core.mail import send_mail
from django.db.models import Avg
from django.conf import settings


@shared_task
def send_monthly_report():
    for user in CustomUser.objects.all():
        student_lessons = StudentLesson.objects.filter(student=user)
        if student_lessons.exists():
            avg_mark = student_lessons.aggregate(avg_mark=Avg('mark'))['avg_mark']
            if avg_mark < 6:
                message = "Не расстраивайтесь, нужно больше стараться"
            elif avg_mark < 8:
                message = "Хорошая работа, но можете и лучше"
            else:
                message = "Отличная работа, так держать!"
            send_mail(
                f'Ваш ежемесячный отчет',
                f'Средний балл: {avg_mark}\n{message}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email]
            )

