from group.models import StudentGroup, StudentLesson, Group
from group.serializers import StudentLessonSerializer, StudentGroupSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Avg


class StudentAverageGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentLessonSerializer
    http_method_names = ['get']

    def get_queryset(self):
        student_id = self.kwargs.get('student_id')
        queryset = StudentLesson.objects.filter(student_id=student_id)
        return queryset

    def list(self, request, *args, **kwargs):
        student_id = self.kwargs.get('student_id')
        queryset = self.get_queryset()
        average_grade = queryset.aggregate(average=Avg('mark'))['average']
        response_data = {'student_id': student_id, 'average_grade': average_grade}
        return Response(response_data)


class AllStudentAverageGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentLessonSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return StudentLesson.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        students = queryset.values('student').annotate(average_grade=Avg('mark'))

        response_data = []
        for student in students:
            student_id = student['student']
            average_grade = student['average_grade'] or 0.0

            response_data.append({
                'student_id': student_id,
                'average_grade': average_grade
            })

        return Response(response_data)


class GroupAverageGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentLessonSerializer
    http_method_names = ['get']

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        if group_id:
            student_ids = StudentGroup.objects.filter(group_id=group_id).values_list('student_id', flat=True)
            return StudentLesson.objects.filter(student_id__in=student_ids)
        else:
            return StudentLesson.objects.none()

    def list(self, request, *args, **kwargs):
        group_id = self.kwargs.get('group_id')
        if group_id:
            queryset = self.get_queryset()
            group_average_grade = queryset.aggregate(average=Avg('mark'))['average']
            response_data = {
                'group_id': group_id,
                'group_average_grade': group_average_grade
            }
            return Response(response_data)
        else:
            return Response({'error': 'Group ID is required'}, status=400)


class AllGroupsAverageGradeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = StudentLessonSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return Group.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = []
        for group in queryset:
            student_ids = StudentGroup.objects.filter(group=group).values_list('student_id', flat=True)
            average_grade = StudentLesson.objects.filter(student__in=student_ids).aggregate(average=Avg('mark'))['average']
            response_data.append({
                'group_id': group.id,
                'group_average_grade': average_grade
            })
        return Response(response_data)

