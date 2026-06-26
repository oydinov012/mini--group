from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.shop.models import (
    Product, Category, Brands, Wishlist, Review,
    Cart, CartItem, ProductImage, Sale, DeliveryAddress
)


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class CategorySeralizer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandsSeralizer(ModelSerializer):
    class Meta:
        model = Brands
        fields = '__all__'


class ProductSeralizer(ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_published=True)
        if not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)


class ProductCompareSerializer(ModelSerializer):
    """Product comparison uchun to'liq ma'lumot"""
    images = ProductImageSerializer(many=True, read_only=True)
    category = CategorySeralizer(read_only=True)
    brand = BrandsSeralizer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_published=True)
        if not reviews.exists():
            return None
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def get_review_count(self, obj):
        return obj.reviews.filter(is_published=True).count()


class WishlistSeralizer(ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'


# ── Review ─────────────────────────────────────────────────────────────────
class ReviewSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'is_published', 'created_at')


class ReviewAdminSerializer(ModelSerializer):
    """Admin uchun — is_published ni o'zgartirish mumkin"""
    class Meta:
        model = Review
        fields = '__all__'


# ── Cart ────────────────────────────────────────────────────────────────────
class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


# ── Sale (Aksiya) ────────────────────────────────────────────────────────────
class SaleSerializer(ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Sale
        fields = '__all__'


# ── DeliveryAddress ──────────────────────────────────────────────────────────
class DeliveryAddressSerializer(ModelSerializer):
    class Meta:
        model = DeliveryAddress
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
