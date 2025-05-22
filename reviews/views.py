from rest_framework import viewsets, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country, Manufacturer, Car, Comment
from .serializers import CountrySerializer, ManufacturerSerializer, CarSerializer, CommentSerializer
import pandas as pd
from django.http import HttpResponse

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(detail=False, methods=['get'], url_path='export', url_name='export')
    def export(self, request):
        try:
            export_type = request.GET.get('type', 'csv').strip().lower()
            queryset = self.filter_queryset(self.get_queryset())

            # Преобразование данных: конвертируем дату в строку или наивный datetime
            data = []
            for comment in queryset:
                item = {
                    "id": comment.id,
                    "email": comment.email,
                    "car": comment.car.name,
                    "text": comment.text,

                    "created_date": comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
                }
                data.append(item)

            df = pd.DataFrame(data)

            if export_type == 'xlsx':
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="comments.xlsx"'
                df.to_excel(response, index=False)
            elif export_type == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="comments.csv"'
                df.to_csv(response, index=False)
            else:
                return Response(
                    {"error": "Неподдерживаемый формат. Используйте 'csv' или 'xlsx'."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)