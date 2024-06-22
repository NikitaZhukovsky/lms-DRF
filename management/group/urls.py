from django.urls import path, include
from rest_framework.routers import DefaultRouter
from group.views.group_lesson_views import GroupViewSet, StudentLessonViewSet
from group.views.student_group_views import StudentGroupView, StudentGroupViewSet
from group.views.average_grade_views import GroupAverageGradeViewSet, StudentAverageGradeViewSet, AllGroupsAverageGradeViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'student-lesson', StudentLessonViewSet, basename='student_lesson')

urlpatterns = [
    path('', include(router.urls)),
    path('student-group/', StudentGroupView.as_view(), name='student_group'),
    path('student-group/<int:student_group_id>/', StudentGroupViewSet.as_view(), name='student_group_set'),
    path('students/<int:student_id>/average-grade/', StudentAverageGradeViewSet.as_view({'get': 'list'}),
         name='student-average-grade'),
    path('groups/<int:group_id>/average-grade/', GroupAverageGradeViewSet.as_view({'get': 'list'}),
         name='group-average-grade'),
    path('average-grade/', AllGroupsAverageGradeViewSet.as_view({'get': 'list'}),
          name='all_groups_average_grade'),
]

