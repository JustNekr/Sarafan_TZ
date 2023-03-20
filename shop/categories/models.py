from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name="название", max_length=64)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    img = models.ImageField(blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(verbose_name="название", max_length=64)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    img = models.ImageField(blank=True, null=True)  # TODO: in 3 sizes
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
