from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'pk',
            'title',
            'writer',
            'description',
            'total_amount',
            'end_date',
            'onetime_amount',
            'now_amount',
        ]

        read_only_fields = ('customers', 'now_amount')


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



    # d_day = serializers.SerializerMethodField(method_name='d_day')
    # achievement_rate = serializers.SerializerMethodField(method_name='achievement_rate')
    # customer_check = serializers.SerializerMethodField(method_name='customer_check')
    #
    # def d_day(self, instance):
    #     return instance.d_day()
    #
    # def achievement_rate(self, instance):
    #     return instance.achievement_rate()
    #
    # def customer_check(self, instance):
    #     return instance.customer_check()

class FundingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [

        ]
