from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country, Manufacturer, Car, Comment
from .services import ExportMixin
from .serializers import CountrySerializer, ManufacturerSerializer, CarSerializer, CommentSerializer
import pandas as pd
from django.http import HttpResponse

class CountryViewSet(ExportMixin, viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ManufacturerViewSet(ExportMixin, viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class CarViewSet(ExportMixin, viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(ExportMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

