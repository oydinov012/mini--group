from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from apps.order.models import PromoCode, Order, OrderItem
 
 
class PromoCodeSeralizer(ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'
        read_only_fields = ('used_count',)
 
 
class OrderItemSeralizer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
 
 
class OrderSeralizer(ModelSerializer):
    items = OrderItemSeralizer(many=True, read_only=True)
 
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'total_amount')
 