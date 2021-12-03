from django.contrib import admin
from django.urls import path
from UserAdministration import views

urlpatterns = [
    path('user-registration/', views.RegisterApi.as_view(), name='user-registration'),
    path('user-login/', views.LoginAPIView.as_view(), name='auth-login'),
]