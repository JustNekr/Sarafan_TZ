import os
import time
from functools import cached_property
from io import StringIO, BytesIO

from PIL import Image
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from rest_framework.reverse import reverse_lazy, reverse


class Category(MPTTModel):
    name = models.CharField(verbose_name="название", max_length=64)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_category',
                            db_index=True, verbose_name='Родительская категория')
    image = models.ImageField(upload_to='img/categories', null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    # def clean(self):
    #     if self.parent and self.parent.level == 1:
    #         raise ValidationError({'parent': 'Достигнута максимальная вложенность!'})


def get_sized_images(image, product_slug):
    max_size = (200, 200)
    medium_size = (100, 100)
    min_size = (50, 50)
    image_max = get_resized_in_memory_upload_file(
        file=image,
        size=max_size,
        size_name='max',
        product_slug=product_slug)  # .thumbnail(max_size)
    image_medium = get_resized_in_memory_upload_file(
        file=image,
        size=medium_size,
        size_name='medium',
        product_slug=product_slug)
    image_min = get_resized_in_memory_upload_file(
        file=image,
        size=min_size,
        size_name='min',
        product_slug=product_slug)
    return image_max, image_medium, image_min


def get_resized_in_memory_upload_file(file, size, size_name, product_slug):
    img = Image.open(file)
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, file.content_type.split('/')[-1].upper())

    new_file_name = str(product_slug) + '_' + str(int(time.time())) + str(size_name) + os.path.splitext(file.name)[1]

    file = InMemoryUploadedFile(file=thumb_io,
                                field_name=u"image_{}".format(size_name),
                                name=new_file_name,
                                content_type=file.content_type,
                                size=thumb_io.getbuffer().nbytes,
                                charset=None)

    return file


def product_image_upload_to(instance, filename):
    product_slug, filename = '_'.join(filename.split('_')[:-1]), filename.split('_')[-1]
    return 'img/products/{0}/{1}'.format(product_slug, filename)


class ProductImage(models.Model):
    image_max = models.ImageField(upload_to=product_image_upload_to)
    image_medium = models.ImageField(upload_to=product_image_upload_to)
    image_min = models.ImageField(upload_to=product_image_upload_to)

    @staticmethod
    def upload_image(image, product_slug):
        image_max, image_medium, image_min = get_sized_images(image, product_slug)

        picture = ProductImage.objects.create(
            image_max=image_max,
            image_medium=image_medium,
            image_min=image_min,
        )
        return picture


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="URL")
    sub_category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',
                                     verbose_name='Подкатегория')  # TODO: check ondelete
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    image = models.ForeignKey(ProductImage, on_delete=models.SET_NULL, blank=True, null=True,
                              related_name='product')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def get_adding_url(self):
        return reverse('basket-add', args=[str(self.slug)])

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.slug)])

    def set_image(self, image):
        if self.image is not None:
            print()
            self.image.delete()
        print()
        self.image = ProductImage.upload_image(image=image, product_slug=self.slug)


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
