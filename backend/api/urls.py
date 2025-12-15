from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Handles POST /token/ (Login)
    TokenRefreshView,     # Handles POST /token/refresh/ (Renewing token)
)

urlpatterns = [
    # ------------------------------------------------------------------
    # 1. Admin Interface (Optional but recommended)
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # 2. Authentication and JWT Endpoints
    # The prefix 'api/v1/auth/' groups all user management and JWT logic.
    # ------------------------------------------------------------------
    path('api/v1/auth/', include([
        
        # JWT Token Endpoints (Login/Refresh)
        # This is where a user exchanges credentials for a token pair.
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

        # App-Specific Authentication Routes (Register/Me)
        # Includes all the paths defined in backend/authentication/urls.py (register/, me/)
        path('', include('authentication.urls')),
    ])),
]