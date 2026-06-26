from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from apps.order.models import Order, OrderItem, PromoCode
from api.serializer.order_app import OrderSeralizer, OrderItemSeralizer, PromoCodeSeralizer
from api.paginations import CustomPagination



class PromoCodeListCreateView(generics.ListCreateAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSeralizer
    permission_classes = [IsAdminUser]


class PromoCodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSeralizer
    permission_classes = [IsAdminUser]


class PromoCodeCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('code')
        if not code:
            return Response({'error': 'PromoCod korsatilmagan.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            promo = PromoCode.objects.get(code=code, is_active=True)
            return Response({
                'valid': True,
                'code': promo.code,
                'discount_value': promo.discount_value,
            })
        except PromoCode.DoesNotExist:
            return Response({'valid': False, 'error': 'PromoCod ishlamiyapti.'}, status=status.HTTP_404_NOT_FOUND)



class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSeralizer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().select_related('user', 'promo_code')
        return Order.objects.filter(user=user).select_related('promo_code')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)


class OrderStatusUpdateView(generics.UpdateAPIView):
    serializer_class = OrderSeralizer
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Notogri status.'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = new_status
        order.save()
        return Response(OrderSeralizer(order).data)



class OrderItemListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderItemSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        return OrderItem.objects.filter(
            order_id=order_id,
            order__user=self.request.user
        ).select_related('product')

    def perform_create(self, serializer):
        order_id = self.kwargs.get('order_id')
        serializer.save(order_id=order_id)


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)