from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from apps.shop.models import Product, ProductImage, Category, Brands, Whishlist, Review, Cart, CartItem
from api.serializer.shop_app import (
    ProductSeralizer, ProductImageSerializer, CategorySeralizer,
    BrandsSeralizer, WhishlistSeralizer, ReviewSerializer,
    CartSerializer, CartItemSerializer
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
        qs = Product.objects.filter(is_active=True).select_related('category', 'brand').prefetch_related('images')
        params = self.request.query_params
        if params.get('category'):
            qs = qs.filter(category_id=params['category'])
        if params.get('brand'):
            qs = qs.filter(brand_id=params['brand'])
        if params.get('min_price'):
            qs = qs.filter(price__gte=params['min_price'])
        if params.get('max_price'):
            qs = qs.filter(price__lte=params['max_price'])
        if params.get('search'):
            qs = qs.filter(name__icontains=params['search'])
        return qs

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().prefetch_related('images')
    serializer_class = ProductSeralizer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


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
    serializer_class = WhishlistSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Whishlist.objects.filter(user=self.request.user).select_related('product')


class WishlistAddView(generics.CreateAPIView):
    serializer_class = WhishlistSeralizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistDeleteView(generics.DestroyAPIView):
    serializer_class = WhishlistSeralizer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Whishlist.objects.filter(user=self.request.user)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_id'], is_published=True)


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


# ── Cart ──────────────────────────────────────────────────────────────────────
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
        return Response({'message': 'Корзина очищена.'}, status=status.HTTP_204_NO_CONTENT)