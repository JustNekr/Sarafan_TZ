from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(verbose_name="название", max_length=64)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    # img = models.ImageField(blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='children',
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

    def save(self, *args, **kwargs):
        if self.parent and self.parent.level == 1:
            raise ValueError(u'Достигнута максимальная вложенность!')
        super(Category, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name="URL")
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='products', verbose_name='Категория')
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0)
    # img = models.ImageField(blank=True, null=True)  # TODO: in 3 sizes

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
