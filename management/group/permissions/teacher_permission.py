from rest_framework.permissions import BasePermission


class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'Teacher'
        return False
