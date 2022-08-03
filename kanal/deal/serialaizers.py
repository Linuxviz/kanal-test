from rest_framework import serializers

from deal.models import Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['table_id', 'order_id', 'usa_dollar_price', 'ruble_price', 'delivery_time', ]
