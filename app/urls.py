from django.urls import path
from .views import UserRegisterView, HydroponicSystemViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'systems', HydroponicSystemViewSet, basename="system")

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register-endpoint"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
