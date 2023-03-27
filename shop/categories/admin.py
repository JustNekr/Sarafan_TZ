from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from django import forms
from .models import Category


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(queryset=Category.objects.filter(parent=None), empty_label="(Nothing)", required=False)

    class Meta:
        model = Category
        fields = ['name', 'slug', 'parent', 'image']


class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("name",)}
    form = CategoryForm


admin.site.register(Category, CategoryAdmin)



