from django.shortcuts import render
from rest_framework import viewsets, generics, filters
# Create your views here.
from .models import Product
from .serializers import ProductSerializer


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    ordering_fields = ['created_at', 'total_amount']
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)