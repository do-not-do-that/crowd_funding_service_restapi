from rest_framework import serializers

from .models import Product

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'writer',
            'description',
            'total_amount',
            'end_date',
            'onetime_amount',
        ]

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'writer',
            'description',
            'end_date',
            'onetime_amount',
        ]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ('total_amount',)
        extra_kwargs = {
            'writer' : {'write_only': True}
        }

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    d_day = serializers.SerializerMethodField(method_name='d_day')
    achievement_rate = serializers.SerializerMethodField(method_name='achievement_rate')
    customer_check = serializers.SerializerMethodField(method_name='customer_check')

    def d_day(self, instance):
        return instance.d_day()

    def achievement_rate(self, instance):
        return instance.achievement_rate()

    def customer_check(self, instance):
        return instance.customer_check()

    def update(self, instance, data):
        instance.now_amount += instance.onetime_amount
        instance.save()
        return super().update(instance, data)