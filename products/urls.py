from django.urls import path, include
from .views import ProductListAPIView
urlpatterns = [
    path('products/', ProductListAPIView.as_view())
]

