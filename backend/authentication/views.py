from django.shortcuts import render
from seriallizers import UserProfileSerializer, UserRegistrationSerializer 
from models import UserManager, User
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.views.decorators.http import require_GET, require_POST
from rest_framework.permissions import IsAuthenticated


@require_POST
class UserRegisterView(CreateAPIView):
    model = UserManager
    serializer_class = UserRegistrationSerializer



@require_GET
class UserProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user
