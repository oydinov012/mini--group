from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from apps.shop.models import Product, Category, Brands, Whishlist, Review, Cart,CartItem
from api.serializer.shop_app import (
    CartItemSerializer, CartSerializer, ProductSeralizer, CategorySeralizer,
    BrandsSeralizer, WhishlistSeralizer, ReviewSerializer
)
from api.paginations import CustomPagination


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySeralizer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySeralizer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]



class BrandsListCreateView(generics.ListCreateAPIView):
    queryset = Brands.objects.filter(is_active=True)
    serializer_class = BrandsSeralizer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class BrandsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brands.objects.all()
    serializer_class = BrandsSeralizer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]



class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSeralizer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).select_related('category', 'brand')

        category = self.request.query_params.get('category')
        brand = self.request.query_params.get('brand')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        search = self.request.query_params.get('search')

        if category:
            qs = qs.filter(category_id=category)
        if brand:
            qs = qs.filter(brand_id=brand)
        if min_price:
            qs = qs.filter(price__gte=min_price)
        if max_price:
            qs = qs.filter(price__lte=max_price)
        if search:
            qs = qs.filter(name__icontains=search)

        return qs

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSeralizer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]




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
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id, is_published=True)


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

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(
            cart__user=self.request.user
        )