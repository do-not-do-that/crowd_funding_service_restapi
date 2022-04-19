from django.urls import path, include
from .views import ProductListView, ProductDetailView, FundingView

urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<int:pk>', ProductDetailView.as_view()),
    path('products/<int:pk>/funding', FundingView.as_view())
]

