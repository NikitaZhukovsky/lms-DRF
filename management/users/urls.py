from django.urls import path, include
from users.views import ActivateUser

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('activate/<str:uid>/<str:token>/', ActivateUser.as_view({'get': 'activation'})),
]
