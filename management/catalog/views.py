from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from catalog.models import Course, CourseModule, Lesson, LessonContent
from catalog.serializers import CourseSerializer, DeleteCourseSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (AllowAny, )


class CourseView(APIView):
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

    def delete(self, request):
        input_serializer = DeleteCourseSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            course = Course.objects.get(id=input_serializer.data["course_id"]).delete()
        return Response()


class CourseUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, course_id):
        user = request.user
        if user.is_staff:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response(status=404)

            input_serializer = CourseSerializer(instance=course, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can update a course.")
