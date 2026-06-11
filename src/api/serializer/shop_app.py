from apps.shop.models import Product, Category, Brands, Whishlist
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
