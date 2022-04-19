from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='writer.nickname')
    class Meta:
        model = Product
        fields = [
            'title',
            'username',
            'description',
            'total_amount',
            'end_date',
            'onetime_amount',
            'now_amount',
            'achievement_rate',
            'd_day'
        ]
        read_only_fields = ('now_amount', )
        extra_kwargs = {
            'description': {'write_only': True},
            'total_amount': {'write_only': True},
            'end_date': {'write_only': True},
            'onetime_amount': {'write_only': True}
        }


class ProductDetailSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='writer.nickname')

    class Meta:
        model = Product
        fields = [
            'title',
            'username',
            'now_amount',
            'achievement_rate',
            'd_day',
            'description',
            'total_amount',
            'customer_check',
            'end_date',
            'onetime_amount',
        ]

        read_only_fields = ('total_amount', 'now_amount')

        extra_kwargs = {
            'end_date' : {'write_only': True},
            'onetime_amount': {'write_only': True}
        }



class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = []
