import os
import time
from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from rest_framework.reverse import reverse

from categories.models import Category


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

