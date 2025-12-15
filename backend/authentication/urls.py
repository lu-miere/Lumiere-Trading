from django.contrib import admin
from django.urls import path, include
from  .views import UserProfileView, UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='registration'),
    path('me/', UserProfileView.as_view(), name='me')
]