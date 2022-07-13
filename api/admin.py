from django.contrib import admin
from api import models


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'brand', 'review_score')
    search_fields = ('title', 'brand')
    list_filter = ('brand',)
    ordering = ('title',)


class ReviewProductAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'text', 'rate')
    search_fields = ('author', 'product', 'text')
    list_filter = ('author', 'product')
    ordering = ('author',)


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('client',)
    search_fields = ('client', 'products')
    list_filter = ('client',)
    ordering = ('client',)


admin.site.register(models.Client, ClientAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ReviewProduct, ReviewProductAdmin)
admin.site.register(models.Wishlist, WishlistAdmin)
