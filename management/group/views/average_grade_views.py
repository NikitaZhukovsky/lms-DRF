from group.models import StudentGroup, StudentLesson
from group.serializers import StudentLessonSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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

