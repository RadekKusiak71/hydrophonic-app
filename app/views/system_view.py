from rest_framework import viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import HydroponicSystemSerializer
from ..models import HydroponicSystem
from ..decorators import is_owner
from rest_framework.pagination import PageNumberPagination
from ..filters import HydroponicSystemFilterSet
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import QuerySet


class HydroponicSystemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 20


class HydroponicSystemViewSet(viewsets.ViewSet):
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]
    pagination_class = HydroponicSystemPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = HydroponicSystemFilterSet

    """
        All methods needs Authorization : Bearer <user_token> in headers
    """

    def list(self, request):
        """
            Method for fetching data about his hydroponic systems
        """
        # Method is fetching systems for currently logged user
        systems = HydroponicSystem.objects.filter(owner=request.user.id)
        filtered_systems = self.filter_queryset(systems)

        # Paginating data
        paginator = self.pagination_class()
        paginated_systems = paginator.paginate_queryset(
            filtered_systems, request, view=self)

        serializer = HydroponicSystemSerializer(paginated_systems, many=True)
        return paginator.get_paginated_response(serializer.data)

    def filter_queryset(self, queryset) -> QuerySet[HydroponicSystem]:
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    def create(self, request):
        """
            Method for creating hydroponic system
        """
        serializer = HydroponicSystemSerializer(
            data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @is_owner
    def retrieve(self, request, pk=None):
        """
            Method for retrieving a data about hydroponic system
        """
        system = get_object_or_404(HydroponicSystem, id=pk)
        serializer = HydroponicSystemSerializer(system)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_owner
    def update(self, request, pk=None):
        """
            Method for updating a whole instance of hydroponic system
        """
        system = get_object_or_404(HydroponicSystem, id=pk)
        serializer = HydroponicSystemSerializer(
            system, data=request.data, partial=False, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_owner
    def partial_update(self, request, pk=None):
        """
            Method for partialy updating a hydroponic system
        """
        system = get_object_or_404(HydroponicSystem, id=pk)
        serializer = HydroponicSystemSerializer(
            system, data=request.data, partial=True, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @is_owner
    def destroy(self, request, pk=None):
        """
            Method for deleting a hydroponic system
        """
        system = get_object_or_404(HydroponicSystem, id=pk)
        system.delete()
        return Response({"detail": "System deleted successfully"}, status=status.HTTP_200_OK)
