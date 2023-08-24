from django.contrib import admin

from shop.models import Category, Flowers


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)
    list_filter = ('name',)
    search_fields = ('name',)
    verbose_name = 'Категории'


@admin.register(Flowers)
class FlowersAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'date_of_creation', 'last_modified_date', 'Imag')
    list_filter = ('category',)
    search_fields = ('name',)
    verbose_name = 'Продукт'
