from rest_framework import serializers
from .models import Product, ProductImage


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




