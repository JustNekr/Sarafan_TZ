from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from django import forms
from .models import Product, Category


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), empty_label="(Nothing)", required=False)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent']


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = CategoryForm


admin.site.register(Category, CategoryAdmin)


class ProductForm(forms.ModelForm):
    sub_category = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None), empty_label="(Nothing)", required=True)

    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'price']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = ProductForm


admin.site.register(Product, ProductAdmin)
