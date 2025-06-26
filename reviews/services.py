from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
import pandas as pd
from django.http import HttpResponse, JsonResponse

class ExportMixin:
    @action(detail=False, methods=['get'], url_path='export', url_name='export')
    def export(self, request):
        export_type = request.GET.get('type', 'json')
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        if export_type == 'xlsx':
            return self._export_xlsx(data)
        elif export_type == 'csv':
            return self._export_csv(data)
        else:
            return JsonResponse(data, safe=False)

    def _export_xlsx(self, data):
        df = pd.json_normalize(data)
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
        df.to_excel(response, index=False)
        return response

    def _export_csv(self, data):
        df = pd.json_normalize(data)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        df.to_csv(response, index=False)
        return response