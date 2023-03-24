from django.db.models import F, Avg
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet
from .models import Product, Category, Basket
from .serializers import ProductSerializer, CategorySerializer, BasketSerializer


class ProductAPIViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Product.objects.all().select_related('sub_category').annotate(category=F('sub_category__parent__name'))
    serializer_class = ProductSerializer


class CategoryAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None).prefetch_related('sub_category')
    serializer_class = CategorySerializer


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class BasketAPIViewSet(mixins.ListModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.DestroyModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated & IsOwner]
    queryset = Basket.objects.all().select_related().annotate(price=F('product__price'))
    serializer_class = BasketSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return self.queryset.filter(user=user) #.aggregate(average_price=Avg('price'))

    # @action(methods=['post'], detail=True, permission_classes=[IsAdminOrIsSelf],
    #         url_path='change-password', url_name='change_password')
    # def set_password(self, request, pk=None):
    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def add(self, request, slug=None):
        product = get_object_or_404(Product, slug=slug)
        item, created = Basket.objects.get_or_create(product=product, user=request.user)
        if not created:
            item.quantity += 1
            item.save()
        if request.META['HTTP_REFERER']:
            return HttpResponseRedirect(redirect_to=request.META['HTTP_REFERER'])
        return HttpResponseRedirect(redirect_to=request.build_absolute_uri(reverse('basket-list')))

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        obj = get_object_or_404(queryset, **{"product__slug": self.kwargs[self.lookup_field]})
        self.check_object_permissions(self.request, obj)
        return obj

