from django.urls import path, include
from users.views import ActivateUser, AddTeacherView, TeacherView, StudentView

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'})),
    path('add-teacher/', AddTeacherView.as_view(), name='add_teacher'),
    path('teachers/', TeacherView.as_view(), name='users'),
    path('students/', StudentView.as_view(), name='student')
]
