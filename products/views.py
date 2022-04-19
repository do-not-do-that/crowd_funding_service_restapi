from django.shortcuts import render
from rest_framework import viewsets, generics, filters, status, permissions
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer, FundingSerializer, ProductDetailSerializer


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    ordering_fields = ['created_at', 'now_amount']
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class FundingView(generics.RetrieveUpdateAPIView):

    queryset = Product.objects.all()
    serializer_class = FundingSerializer

    # 로그인된 사용자만
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        product.customers.add(request.user)
        product.now_amount += product.onetime_amount
        product.save()
        return Response(status=status.HTTP_200_OK)


