from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('sub_category')
    serializer_class = CategorySerializer
