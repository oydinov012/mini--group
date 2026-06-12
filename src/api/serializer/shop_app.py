from apps.shop.models import Product, Category, Brands, Whishlist, Review
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


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user', 'is_published', 'created_at')
