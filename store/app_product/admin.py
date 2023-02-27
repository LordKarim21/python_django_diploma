from django.contrib import admin
from .models import Product, ImageProduct, Comment, Tag, Category, SaleProduct


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'archived']


class ImageProductAdmin(admin.ModelAdmin):
    list_display = ['image', 'product', ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'review']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


class SaleProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'started_sale', 'finished_sale']


admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ImageProduct, ImageProductAdmin)
admin.site.register(Product, ProductAdmin)
