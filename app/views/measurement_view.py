from rest_framework import generics, status
from rest_framework.response import Response
from ..serializers import MeasurementSerializer
from ..models import HydroponicSystem, Measurement
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from ..filters import MeasurementSystemFilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import PermissionDenied


class MeasurementPagination(PageNumberPagination):
    # Page size can be adjusted
    page_size = 20
    page_size_query_param = 'page_size'


class ListMeasurementView(generics.ListAPIView):
    """
        Listing measurements for a hydroponic system

        for ascending order just place - before field name in url
        for descdening order is default ( without a - or + char)
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    pagination_class = MeasurementPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MeasurementSystemFilterSet

    def get_queryset(self):
        system = HydroponicSystem.objects.get(id=self.kwargs.get("pk"))
        if system.owner != self.request.user:
            raise PermissionDenied()
        return Measurement.objects.filter(system=system)


class ListLatestMeasurementView(generics.ListAPIView):
    """
        Listing last 10 measurements for a hydroponic system

        for ascending order just place - before field name in url
        for descdening order is default ( without a - or + char)
    """
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MeasurementSystemFilterSet

    def get_queryset(self):
        system = HydroponicSystem.objects.get(id=self.kwargs.get("pk"))
        if system.owner != self.request.user:
            raise PermissionDenied()
        return Measurement.objects.filter(system=system)[:10]


class CreateMeasurementView(generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
