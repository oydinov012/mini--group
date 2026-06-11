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


class OrderItemSeralizer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = '__all__'