from functools import cached_property

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework.reverse import reverse_lazy, reverse


class Category(MPTTModel):
    name = models.CharField(verbose_name="название", max_length=64)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # img = models.ImageField(blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_category',
                            db_index=True, verbose_name='Родительская категория')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    # def get_absolute_url(self):
    #     return reverse('post-by-category', args=[str(self.slug)])
    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.parent and self.parent.level == 1:
    #         raise ValidationError({'parent': 'Достигнута максимальная вложенность!'})


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="URL")
    sub_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products', verbose_name='Подкатегория')
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    # img = models.ImageField(blank=True, null=True)  # TODO: in 3 sizes

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_adding_url(self):
        # return f"https://{Site.objects.get_current().domain}{reverse('basket-add', args=[str(self.slug)])}"
        return reverse('basket-add', args=[str(self.slug)])

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.slug)])


    # def clean(self):
    #     if self.sub_category.parent == None:
    #         raise ValidationError({'sub_category': 'Требуется подкатегория'})


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=1)

    class Meta:
        unique_together = [['user', 'product']]
        verbose_name = 'Товар'
        verbose_name_plural = 'Корзина'

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @cached_property
    def get_items_cached(self):
        return self.user.basket.select_related()

    @property
    def total_quantity(self):
        _items = self.get_items_cached
        #        _items = Basket.objects.filter(user=self.user)
        _totalquantity = sum(list(map(lambda x: x.quantity, _items)))
        return _totalquantity

    @property
    def total_cost(self):
        _items = self.get_items_cached
        #        _items = Basket.objects.filter(user=self.user)
        _totalcost = sum(list(map(lambda x: x.product_cost, _items)))
        return _totalcost

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user).order_by('product__sub_category')

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk)


