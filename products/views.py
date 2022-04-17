from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product
    serializer_class =