from django.urls import path
from .views import UserRegisterView, ListLatestMeasurementView, HydroponicSystemViewSet, ListMeasurementView, CreateMeasurementView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Hydrophonic Service Api",
        default_version='v1',
        description="Hydrophonic Service Api",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="radoslawkusiak7171@gmail.com"),
        license=openapi.License(
            name="Just have fun with it if you want to :)"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


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

    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),

]

urlpatterns += router.urls
