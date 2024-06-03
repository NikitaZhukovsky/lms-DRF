from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from catalog.models import Course, CourseModule, Lesson, LessonContent
from catalog.serializers import CourseSerializer, CourseModuleSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (AllowAny, )


class AddCourseView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        input_serializer = CourseSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add course.")


class CourseView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        serializer = CourseSerializer(course, many=True)
        return Response(serializer.data)

    def put(self, request, course_id):
        user = request.user
        if user.is_staff:
            course = get_object_or_404(Course, id=course_id)
            input_serializer = CourseSerializer(instance=course, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can update a course.")

    def delete(self, request, course_id):
        user = request.user
        if user.is_staff:
            get_object_or_404(Course, id=course_id).delete()
            return Response()
        else:
            raise PermissionDenied("Only staff users can delete a course")


class AddCourseModuleView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        input_serializer = CourseModuleSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add module.")


class CourseModuleView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        serializer = CourseModuleSerializer(module, many=True)
        return Response(serializer.data)

    def put(self, request, module_id):
        user = request.user
        if user.is_staff:
            module = get_object_or_404(CourseModule, id=module_id)
            input_serializer = CourseModuleSerializer(instance=module, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can update a module.")

    def delete(self, request, module_id):
        user = request.user
        if user.is_staff:
            get_object_or_404(CourseModule, id=module_id).delete()
            return Response()

        else:
            raise PermissionDenied("Only staff users can delete a module")



