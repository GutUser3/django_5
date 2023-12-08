from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/register/', views.RegisterAPIView.as_view()),
    path('api/v1/users/login/', views.AuthAPIView.as_view()),
    path('api/v1/users/confirm/', views.ConfirmAPIView.as_view()),
]