from rest_framework import serializers
from .models import Product, Category, Basket, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ['id']


class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    url = serializers.SerializerMethodField()
    image = ProductImageSerializer()

    class Meta:
        model = Product
        fields = ('name', 'category', 'sub_category', 'price', 'url', 'image')
        depth = 1

    def get_url(self, product):
        request = self.context.get('request')
        product_url = product.get_adding_url()

        return request.build_absolute_uri(product_url)


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    sub_category = SubCategorySerializer(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'sub_category', 'image')


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

