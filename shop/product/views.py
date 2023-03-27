from django.db.models import F
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Product
from .serializers import ProductSerializer


class ProductAPIViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all().select_related('sub_category').annotate(category=F('sub_category__parent__name'))
    serializer_class = ProductSerializer

