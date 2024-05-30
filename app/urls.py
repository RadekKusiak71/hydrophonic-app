from django.urls import path
from .views import UserRegisterView, ListLatestMeasurementView, HydroponicSystemViewSet, ListMeasurementView, CreateMeasurementView
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

    # Measurement paths
    path("measurements/", CreateMeasurementView.as_view(),
         name="create-measurement"),
    path("measurements/system/<int:pk>/", ListMeasurementView.as_view(),
         name="list-measurement"),
    path("measurements/system/<int:pk>/latest/", ListLatestMeasurementView.as_view(),
         name="list-latest-measurement"),


]

urlpatterns += router.urls
