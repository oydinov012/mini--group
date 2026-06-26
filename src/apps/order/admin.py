from django.contrib import admin
from apps.order.models import PromoCode, Order, OrderItem
# Register your models here.

admin.site.register(PromoCode)
admin.site.register(Order)
admin.site.register(OrderItem)
