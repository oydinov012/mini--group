from django.db.models import Avg, Count, Q
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from apps.shop.models import (
    Product, ProductImage, Category, Brands,
    Wishlist, Review, Cart, CartItem, Sale, DeliveryAddress
)
from api.serializer.shop_app import (
    ProductSeralizer, ProductCompareSerializer, ProductImageSerializer,
    CategorySeralizer, BrandsSeralizer, WishlistSeralizer,
    ReviewSerializer, ReviewAdminSerializer,
    CartSerializer, CartItemSerializer,
    SaleSerializer, DeliveryAddressSerializer,
)
from api.paginations import CustomPagination


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySeralizer
    pagination_class = CustomPagination

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySeralizer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]

class BrandsListCreateView(generics.ListCreateAPIView):
    queryset = Brands.objects.filter(is_active=True)
    serializer_class = BrandsSeralizer
    pagination_class = CustomPagination

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class BrandsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandsSeralizer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSeralizer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images', 'reviews')
        p = self.request.query_params
        if p.get('category'):
            qs = qs.filter(category_id=p['category'])
        if p.get('brand'):
            qs = qs.filter(brand_id=p['brand'])
        if p.get('min_price'):
            qs = qs.filter(price__gte=p['min_price'])
        if p.get('max_price'):
            qs = qs.filter(price__lte=p['max_price'])
        if p.get('search'):
            qs = qs.filter(
                Q(name__icontains=p['search']) |
                Q(title__icontains=p['search']) |
                Q(description__icontains=p['search'])
            )
        ordering = p.get('ordering', '-created_at')
        allowed = ['price', '-price', 'created_at', '-created_at', 'name', '-name']
        if ordering in allowed:
            qs = qs.order_by(ordering)
        return qs

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().select_related('category', 'brand').prefetch_related('images', 'reviews')
    serializer_class = ProductSeralizer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


# ── Product Compare ───────────────────────────────────────────────────────────
class ProductCompareView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ids_param = request.query_params.get('ids', '')
        if not ids_param:
            return Response(
                {'error': "ids parametrini ko'rsating. Masalan: ?ids=1,2,3"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            ids = [int(i.strip()) for i in ids_param.split(',') if i.strip()]
        except ValueError:
            return Response(
                {'error': "ids faqat raqamlardan iborat bo'lishi kerak."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(ids) < 2:
            return Response(
                {'error': "Kamida 2 ta mahsulot IDsini ko'rsating."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if len(ids) > 4:
            return Response(
                {'error': "Maksimal 4 ta mahsulot solishtirish mumkin."},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(
            id__in=ids, is_active=True
        ).select_related('category', 'brand').prefetch_related('images', 'reviews')

        if products.count() != len(ids):
            found_ids = list(products.values_list('id', flat=True))
            missing = [i for i in ids if i not in found_ids]
            return Response(
                {'error': f"Quyidagi mahsulotlar topilmadi: {missing}"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductCompareSerializer(products, many=True, context={'request': request})
        return Response({
            'count': len(ids),
            'products': serializer.data
        })


class ProductImageListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_id'])

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_id'])


class ProductImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminUser]

class WishlistListView(generics.ListAPIView):
    serializer_class = WishlistSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class WishlistAddView(generics.CreateAPIView):
    serializer_class = WishlistSeralizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDeleteView(generics.DestroyAPIView):
    serializer_class = WishlistSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Review.objects.filter(
            product_id=self.kwargs['product_id'], is_published=True
        ).select_related('user').order_by('-created_at')


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)


class ReviewAdminListView(generics.ListAPIView):
    serializer_class = ReviewAdminSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Review.objects.select_related('user', 'product').order_by('-created_at')
        is_pub = self.request.query_params.get('is_published')
        if is_pub is not None:
            qs = qs.filter(is_published=is_pub.lower() == 'true')
        return qs


class ReviewAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewAdminSerializer
    permission_classes = [IsAdminUser]
    queryset = Review.objects.all()


class ReviewPublishView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            return Response({'error': 'Review topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        review.is_published = not review.is_published
        review.save(update_fields=['is_published'])
        return Response({
            'id': review.id,
            'is_published': review.is_published,
            'message': f"Review {'tasdiqlandi' if review.is_published else 'bekor qilindi'}."
        })


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart


class CartItemAddView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data.get('quantity', 1)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            item.quantity += quantity
            item.save()


class CartItemUpdateView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartClearView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({'message': 'Savat tozalandi.'}, status=status.HTTP_204_NO_CONTENT)


class SaleListCreateView(generics.ListCreateAPIView):
    serializer_class = SaleSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]

    def get_queryset(self):
        now = timezone.now()
        return Sale.objects.filter(
            is_active=True,
            start_date__lte=now,
            end_date__gte=now,
        ).select_related('product').order_by('-created_at')


class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)


class DeliveryAddressSetDefaultView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            address = DeliveryAddress.objects.get(pk=pk, user=request.user)
        except DeliveryAddress.DoesNotExist:
            return Response({'error': 'Manzil topilmadi.'}, status=status.HTTP_404_NOT_FOUND)
        DeliveryAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save(update_fields=['is_default'])
        return Response({'message': "Default manzil o'rnatildi.", 'id': address.id})


class HomePageView(APIView):
    """
    GET /api/v1/home/
    Top 10: categories, news, popular products, best-sellers
    """
    permission_classes = [AllowAny]

    def get(self, request):
        from apps.news.models import News
        from apps.order.models import OrderItem
        from api.serializer.news_app import NewsSerializer

        # Top 10 kategoriyalar (eng ko'p mahsulot bor)
        categories = Category.objects.filter(is_active=True).annotate(
            product_count=Count('products')
        ).order_by('-product_count')[:10]

        # So'nggi 10 ta yangilik
        news = News.objects.filter(is_published=True).order_by('-created_at')[:10]

        # Eng mashhur (wishlistga eng ko'p qo'shilgan) 10 ta mahsulot
        popular = Product.objects.filter(is_active=True).annotate(
            wish_count=Count('wishlists')
        ).order_by('-wish_count')[:10]

        # Eng ko'p sotilgan 10 ta mahsulot (order items dan)
        from django.db.models import Sum
        best_seller_ids = (
            OrderItem.objects
            .values('product_id')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')
            .values_list('product_id', flat=True)[:10]
        )
        # IDlar tartibini saqlab query
        best_sellers_qs = Product.objects.filter(id__in=best_seller_ids, is_active=True)
        best_sellers_map = {p.id: p for p in best_sellers_qs}
        best_sellers = [best_sellers_map[pk] for pk in best_seller_ids if pk in best_sellers_map]

        # Aktiv aksiyalar
        now = timezone.now()
        sales = Sale.objects.filter(
            is_active=True, start_date__lte=now, end_date__gte=now
        ).select_related('product')[:10]

        return Response({
            'categories': CategorySeralizer(categories, many=True, context={'request': request}).data,
            'latest_news': NewsSerializer(news, many=True, context={'request': request}).data,
            'popular_products': ProductSeralizer(popular, many=True, context={'request': request}).data,
            'best_sellers': ProductSeralizer(best_sellers, many=True, context={'request': request}).data,
            'active_sales': SaleSerializer(sales, many=True, context={'request': request}).data,
        })
