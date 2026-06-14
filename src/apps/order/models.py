from django.db import models
from apps.users.models import User
from apps.shop.models import Product, Category, Brands, Whishlist

# Create your models here.

class PromoCode(models.Model):
    max_use = models.PositiveIntegerField(default=1,)
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

class Order(models.Model):
    status_choices = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    payment_method_choices = [
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('online', 'Online Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=50, choices=payment_method_choices, blank=True, null=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)  
    customer_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)                                       

    def __str__(self):
        return f"Order #{self.id} by {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"