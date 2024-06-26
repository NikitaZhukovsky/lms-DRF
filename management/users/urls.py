from django.urls import path, include
from users.views import ActivateUser, AddTeacherView, TeacherViewSet, StudentViewSet, UserUpdateView, TestLoginView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'})),
    path('add-teacher/', AddTeacherView.as_view(), name='add_teacher'),
    path('update/profile/', UserUpdateView.as_view(), name='user-update'),
    path('test-login/', TestLoginView.as_view(), name='test-login'),
    path('', include(router.urls))
]
