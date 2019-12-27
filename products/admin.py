from django.contrib import admin
from .models import Products, Categories, subCategories, sub_subCategories

# Register your models here.


class product_Admin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'seller_id', 'slug', 'category',
                    'subcategory', 'brand', 'price', 'created_date', 'status')
    list_display_links = ('product_name', 'category',
                          'subcategory', 'brand',)
    ordering = ('id',)
    exclude = ('slug','product_id')


class category_Admin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    ordering = ('id',)


class subCategory_Admin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')
    list_display_links = ('category', 'name',)
    ordering = ('id',)


class sub_subCategories_Admin(admin.ModelAdmin):
    list_display = ('id', 'category', 'name')
    list_display_links = ('category', 'name',)
    ordering = ('id',)


admin.site.register(Products, product_Admin)
admin.site.register(Categories, category_Admin)
admin.site.register(subCategories, subCategory_Admin)
admin.site.register(sub_subCategories, sub_subCategories_Admin)
