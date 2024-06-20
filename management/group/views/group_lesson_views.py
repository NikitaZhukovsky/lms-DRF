from group.models import Group, StudentLesson
from group.serializers import (GroupSerializer, StudentLessonSerializer)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from group.permissions.teacher_permission import IsTeacherOrAdmin


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'put', 'head', 'options', 'delete']


class StudentLessonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]
    queryset = StudentLesson.objects.all()
    serializer_class = StudentLessonSerializer
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ['get', 'post', 'put', 'head', 'options', 'delete']
