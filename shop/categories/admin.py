from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from django import forms
from .models import Product, Category, ProductImage


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), empty_label="(Nothing)", required=False)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image']


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = CategoryForm


admin.site.register(Category, CategoryAdmin)


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
