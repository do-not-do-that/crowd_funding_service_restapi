from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.nickname')
    class Meta:
        model = Product
        fields = '__all__'