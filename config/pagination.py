from config import settings
from drf_yasg import openapi
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework import serializers

class Paginator(PageNumberPagination):
    page_size = settings.REST_FRAMEWORK.get('PAGE_SIZE', 10)
    page_size_query_param = 'page_size'
    max_page_size = 100
    PARAMETERS_DOCS = [
        openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
        openapi.Parameter('page_size', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Results per page'),
    ]

    # def get_response_schema(description, serializer_class:serializers.ModelSerializer, obj={}):
    #     return openapi.Schema(
    #         type=openapi.TYPE_OBJECT,
    #         properties={
    #             "count": openapi.Schema(type=openapi.TYPE_INTEGER),
    #             "page": openapi.Schema(type=openapi.TYPE_INTEGER),
    #             "page_size": openapi.Schema(type=openapi.TYPE_INTEGER),
    #             "results": openapi.Schema(
    #                 type=openapi.TYPE_ARRAY,
    #                 items=openapi.Schema(
    #                     type=openapi.TYPE_OBJECT,
    #                     properties=serializer_class().get_fields() if hasattr(serializer_class, 'get_fields') else obj
    #                 )
    #             )
    #         }
    #     )

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'results': data
        })
