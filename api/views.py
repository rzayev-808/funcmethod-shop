from django.shortcuts import render
from rest_framework import routers, serializers, viewsets,permissions
from .api import *
from catalog.models import *
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .negotiation import IgnoreClientContentNegotiation
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            #'page_size': self.page_size,
            'results': data
        })
class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass



class ProductFilter(filters.FilterSet):

    colorsType_id_in = NumberInFilter(field_name='colors', lookup_expr='in')
    price = filters.RangeFilter()
    class Meta:
        model = Product
        fields = ['colorsType_id_in', 'price','brand','category',]

class ProductsApiViews(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class  = ProductSerializers
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = ProductFilter
    pagination_class = CustomPagination




class SubCategoryApiViews(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class  = SubcategorySerializers
    queryset = SubCategory.objects.all()
    #filter_backends = (DjangoFilterBackend,)
    #filter_class = ProductFilter
    #pagination_class = CustomPagination

class BrandApiViews(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class  = BrandSerializers
    queryset = Brand.objects.all()
    #filter_backends = (DjangoFilterBackend,)
    #filter_class = ProductFilter
    #pagination_class = CustomPagination
