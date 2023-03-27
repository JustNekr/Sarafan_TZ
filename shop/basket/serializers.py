from rest_framework import serializers
from .models import Basket


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ('product', 'quantity')
        depth = 1
        lookup_field = 'slug'
        read_only_fields = ['product']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product_cost'] = instance.product_cost
        return representation

