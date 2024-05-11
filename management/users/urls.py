from django.urls import path, include
from users.views import ActivateUser, AddTeacherView, get_csrf_token

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'})),
    path('get-csrf-token/', get_csrf_token, name='get-csrf-token'),
    path('add-teacher/', AddTeacherView.as_view, name='add_teacher')
]
