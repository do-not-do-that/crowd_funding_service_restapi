from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.nickname')
    class Meta:
        model = Product
        fields = '__all__'