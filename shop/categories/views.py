from django.db.models import F
from rest_framework import generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.views import APIView

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all().select_related('sub_category').annotate(category=F('sub_category__parent__name'))
    serializer_class = ProductSerializer


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('sub_category')
    serializer_class = CategorySerializer


class Basket(CreateModelMixin, APIView):
    pass

# @login_required
# def basket_add(request, pk):
#     if 'login' in request.META.get('HTTP_REFERER'):
#         return HttpResponseRedirect(reverse('products:product', args=[pk]))
#
#     product = get_object_or_404(Product, pk=pk)
#     basket = Basket.objects.filter(user=request.user, product=product).first()
#
#     if not basket:
#         basket = Basket(user=request.user, product=product)
#
#     basket.quantity += 1
#     basket.save()
#
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))