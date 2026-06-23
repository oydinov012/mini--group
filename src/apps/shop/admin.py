from django.contrib import admin
from apps.shop.models import Category, Brands, Product, Wishlist, Review
# Register your models here.

admin.site.register(Category)
admin.site.register(Brands)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Review)