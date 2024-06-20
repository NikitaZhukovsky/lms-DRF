from group.models import StudentGroup
from group.serializers import StudentGroupSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from group.tasks import update_course_notif, delete_course_notif
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404


class StudentGroupView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(request_body=StudentGroupSerializer)
    def post(self, request):
        input_serializer = StudentGroupSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            student_group = input_serializer.save()
            group_id = student_group.group.id
            student_id = student_group.student.id
            update_course_notif(group_id, student_id)
            return Response(input_serializer.data)
        else:
            raise PermissionDenied("Only staff users can add course.")

    def get(self, request):
        queryset = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(queryset, many=True)
        return Response(serializer.data)


class StudentGroupViewSet(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, student_group_id):
        course = get_object_or_404(StudentGroup, id=student_group_id)
        serializer = StudentGroupSerializer(course)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=StudentGroupSerializer)
    def put(self, request, student_group_id):
        course = get_object_or_404(StudentGroup, id=student_group_id)
        input_serializer = StudentGroupSerializer(instance=course, data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        return Response()

    def delete(self, request, student_group_id):
        student_group = get_object_or_404(StudentGroup, id=student_group_id)
        delete_course_notif(student_group)
        student_group.delete()
        return Response()
