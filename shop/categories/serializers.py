from rest_framework import serializers
from .models import Product, Category, Basket


class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    # url = serializers.URLField(source='get_absolute_url')  # , read_only=False)
    # url = serializers.HyperlinkedIdentityField(view_name='basket-add', lookup_field='slug')
    url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('name', 'category', 'sub_category', 'price', 'url')

    def get_url(self, product):
        request = self.context.get('request')
        product_url = product.get_adding_url()

        return request.build_absolute_uri(product_url)




class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = ('name', 'slug', 'sub_category')
        # depth = 1


class BasketSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
   # product = Hyper

    class Meta:
        model = Basket
        fields = ('product', 'quantity')
        depth = 0

