from django.db.models import F
from django.http import HttpResponseRedirect
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from product.models import Product
from .models import Basket
from .serializers import BasketSerializer


class IsOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class BasketAPIViewSet(
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
        return self.queryset.filter(user=user)

    @action(methods=['get'], detail=True)
    def add(self, request, slug=None):
        print()
        product = get_object_or_404(Product, slug=slug)
        item, created = Basket.objects.get_or_create(product=product, user=request.user)
        if not created:
            item.quantity += 1
            item.save()
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            return HttpResponseRedirect(redirect_to=referer)
        return HttpResponseRedirect(redirect_to=request.build_absolute_uri(reverse('basket-list')))

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        obj = get_object_or_404(queryset, **{"product__slug": self.kwargs[self.lookup_field]})
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if serializer.data:
            total_cost = queryset.first().total_cost
            total_quantity = queryset.first().total_quantity
            data = serializer.data
            new_data = {'products_list': data,
                        'total_coast': total_cost,
                        'total_quantity': total_quantity}
            return Response(new_data)
        else:
            return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def delete_all(self, request):
        Basket.objects.filter(user=request.user).delete()
        referer = request.META.get('HTTP_REFERER', '')
        if referer:
            return HttpResponseRedirect(redirect_to=referer)
        return HttpResponseRedirect(redirect_to=request.build_absolute_uri(reverse('basket-list')))
