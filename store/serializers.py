from rest_framework import serializers
from . import models
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title','slug','description', 'unit_price','price_with_tax','inventory', 'collection']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=models.Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product:models.Product):
        return product.unit_price * Decimal(1.1)
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['id', 'name', 'description', 'date']
        
    def create(self, validated_data):
        product_id = self.context['product_id']
        return models.Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id']
        
    id = serializers.UUIDField(read_only=True)
        
    