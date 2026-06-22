from apps.shop.models import Product, Category, Brands, Whishlist, Review, Cart, CartItem, ProductImage
from rest_framework.serializers import ModelSerializer

class ProductSeralizer(ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CategorySeralizer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class BrandsSeralizer(ModelSerializer):

    class Meta:
        model = Brands
        fields = '__all__'
        

class WhishlistSeralizer(ModelSerializer):

    class Meta:
        model = Whishlist
        fields = '__all__'


class ProductImageSerializer(ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'is_published', 'created_at')

class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
