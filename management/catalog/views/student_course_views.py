from rest_framework.views import APIView
from catalog.models import StudentCourse
from catalog.serializers import StudentCourseSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from django.shortcuts import get_object_or_404
from catalog.tasks import update_course_notif, delete_course_notif
from drf_yasg.utils import swagger_auto_schema


class StudentCourseView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=StudentCourseSerializer)
    def post(self, request):
        user = request.user
        if user.is_staff:
            input_serializer = StudentCourseSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            student = input_serializer.validated_data['student']
            course = input_serializer.validated_data['course']
            student.role = 'Student'
            student.save()
            input_serializer.save()
            update_course_notif(student.id, course.id)
            return Response()
        else:
            raise PermissionDenied("Only staff users can add students to courses.")


class StudentCourseViewSet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student_course_id):
        try:
            student_courses = StudentCourse.objects.get(id=student_course_id)
            serializer = StudentCourseSerializer(student_courses)
            return Response(serializer.data)
        except StudentCourse.DoesNotExist:
            raise NotFound(f"No student-course relationships found.")

    @swagger_auto_schema(request_body=StudentCourseSerializer)
    def put(self, request, student_course_id):
        try:
            student_course = get_object_or_404(StudentCourse, id=student_course_id)
            serializer = StudentCourseSerializer(student_course, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except StudentCourse.DoesNotExist:
            raise NotFound(
                f"No student-course relationship found.")

    def delete(self, request, student_course_id):
        try:
            student_course = get_object_or_404(StudentCourse, id=student_course_id)
            student_id = student_course.student_id
            course_id = student_course.course_id
            delete_course_notif(student_id, course_id)
            student_course.delete()
            return Response(status=204)
        except StudentCourse.DoesNotExist:
            raise NotFound("No student-course relationship found.")
