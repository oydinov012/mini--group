from rest_framework.serializers import ModelSerializer
from apps.order.models import PromoCode, Order, OrderItem

class PromoCodeSeralizer(ModelSerializer):
    class Meta:
        model = PromoCode
        fields = '__all__'


class OrderSeralizer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')



class OrderItemSeralizer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('created_at',)