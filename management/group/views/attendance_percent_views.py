from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework.views import APIView
from group.models import StudentLesson
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class AttendancePercentageView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser, ]

    def get(self, request):

        students_attendance = StudentLesson.objects.values('student').annotate(
            total_lessons=Count('lesson'),
            attended_lessons=Count('lesson', filter=Q(attendance=True))
        )

        attendance_percentage = []
        for student_attendance in students_attendance:
            student_id = student_attendance['student']
            total_lessons = student_attendance['total_lessons']
            attended_lessons = student_attendance['attended_lessons']

            percentage = (attended_lessons / total_lessons) * 100 if total_lessons > 0 else 0

            attendance_percentage.append({
                'student_id': student_id,
                'attendance_percentage': percentage
            })

        return JsonResponse({'attendance_percentage': attendance_percentage})
