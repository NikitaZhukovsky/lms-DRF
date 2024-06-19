from django.urls import path, include
from rest_framework.routers import DefaultRouter
from group.views import (GroupViewSet, StudentGroupViewSet, StudentLessonViewSet, StudentAverageGradeViewSet,
                         GroupAverageGradeViewSet)

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'student-groups', StudentGroupViewSet, basename='student_group')
router.register(r'student-lesson', StudentLessonViewSet, basename='student_lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:student_id>/average-grade/', StudentAverageGradeViewSet.as_view({'get': 'list'}),
         name='student-average-grade'),
    path('<int:group_id>/average-grade/', GroupAverageGradeViewSet.as_view({'get': 'list'}))
]
