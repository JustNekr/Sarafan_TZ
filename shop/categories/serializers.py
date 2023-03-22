from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category', 'sub_category', 'price')


class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'sub_category')
