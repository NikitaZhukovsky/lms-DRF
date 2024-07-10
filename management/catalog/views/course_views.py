from rest_framework.views import APIView
from catalog.models import Course
from catalog.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class CourseView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method == 'GET':
            return [IsAuthenticated()]
        return []

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        input_serializer = CourseSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            input_serializer.save()
            return Response(input_serializer.data)
        else:
            raise PermissionDenied("Only staff users can add course.")

    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseViewSet(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        input_serializer = CourseSerializer(instance=course, data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return Response(input_serializer.data)

    def delete(self, request, course_id):
        get_object_or_404(Course, id=course_id).delete()
        return Response()
