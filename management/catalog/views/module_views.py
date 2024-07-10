from rest_framework.views import APIView
from catalog.models import CourseModule
from catalog.serializers import CourseModuleSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema


class CourseModuleView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method == 'GET':
            return [IsAuthenticated()]
        return []

    @swagger_auto_schema(request_body=CourseModuleSerializer)
    def post(self, request):
        input_serializer = CourseModuleSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = request.user
        if user.is_staff:
            input_serializer.save()
            return Response()
        else:
            raise PermissionDenied("Only staff users can add module.")

    def get(self, request):
        queryset = CourseModule.objects.all()
        serializer = CourseModuleSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseModuleViewSet(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated()]
        elif self.request.method == 'PUT':
            return [IsAuthenticated(), IsAdminUser()]
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), IsAdminUser()]
        return []

    def get(self, request, module_id):
        module = get_object_or_404(CourseModule, id=module_id)
        serializer = CourseModuleSerializer(module)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CourseModuleSerializer)
    def put(self, request, module_id):
        user = request.user
        if user.is_staff:
            module = get_object_or_404(CourseModule, id=module_id)
            input_serializer = CourseModuleSerializer(instance=module, data=request.data)
            input_serializer.is_valid(raise_exception=True)
            input_serializer.save()
            return Response(input_serializer.data)
        else:
            raise PermissionDenied("Only staff users can update a module.")

    def delete(self, request, module_id):
        user = request.user
        if user.is_staff:
            get_object_or_404(CourseModule, id=module_id).delete()
            return Response()

        else:
            raise PermissionDenied("Only staff users can delete a module")
