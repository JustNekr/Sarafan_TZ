from django.contrib import admin
from django import forms

from categories.models import Category
from .models import Product


class ProductForm(forms.ModelForm):
    sub_category = forms.ModelChoiceField(queryset=Category.objects.exclude(parent=None), empty_label="(Nothing)", required=True)
    my_image = forms.ImageField()

    class Meta:
        model = Product
        fields = ['name', 'slug', 'sub_category', 'price', 'my_image']


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = ProductForm

    def save_model(self, request, obj, form, change):
        if form.files['my_image'] is not None:
            obj.set_image(form.files['my_image'])
        obj.save()


admin.site.register(Product, ProductAdmin)
