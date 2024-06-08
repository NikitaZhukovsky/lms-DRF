from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from catalog.models import Course, CourseModule, Lesson, LessonContent
from catalog.serializers import CourseSerializer, CourseModuleSerializer, LessonSerializer, LessonContentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage


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
        serializer = CourseSerializer(course)
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


class ModuleListView(ListAPIView):
    queryset = CourseModule.objects.all()
    serializer_class = CourseModuleSerializer
    permission_classes = (IsAuthenticated, )


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
        serializer = CourseModuleSerializer(module)
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


class LessonListView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, )


class AddLessonView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        input_serializer = LessonSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff or user.role == "Teacher":
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add lesson.")


class LessonView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, lesson_id):
        lesson = get_object_or_404(Lesson, id=lesson_id)
        serializer = LessonSerializer(lesson)
        return Response(serializer.data)

    def put(self, request, lesson_id):
        user = request.user
        if user.is_staff or user.role == "Teacher":
            lesson = get_object_or_404(Lesson, id=lesson_id)
            input_serializer = LessonSerializer(instance=lesson, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users and teacher can update lesson.")

    def delete(self, request, lesson_id):
        user = request.user
        if user.is_staff or user.role == "Teacher":
            get_object_or_404(Lesson, id=lesson_id).delete()
            return Response()
        else:
            raise PermissionDenied("Only staff users and teachers can delete lesson.")


class LessonContentViewSet(viewsets.ModelViewSet):
    queryset = LessonContent.objects.all()
    serializer_class = LessonContentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
