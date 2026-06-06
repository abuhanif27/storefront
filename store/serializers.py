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

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'title', 'unit_price']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItem
        fields = ['id', 'product', 'quantity','total_price']
        
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart_item: models.CartItem):
        return cart_item.quantity * cart_item.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cart
        fields = ['id','cartitem_set', 'total_price']
        
    id = serializers.UUIDField(read_only=True)
    cartitem_set = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='calculate_total_price')

    def calculate_total_price(self, cart: models.Cart):
        total_price = Decimal(0)
        for item in cart.cartitem_set.all():
            total_price += item.quantity * item.product.unit_price
        return total_price

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = models.CartItem
        fields = ['id', 'product_id', 'quantity']
    
    def validate_product_id(self, value):
        if not models.Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No product with the given id was found.')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = models.CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except models.CartItem.DoesNotExist:
            self.instance = models.CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance