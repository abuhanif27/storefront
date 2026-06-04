from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import ProductFilter
from . import models
from .paginations import CustomPagination
from . import serializers

# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if models.OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    
class CollectionViewSet(ModelViewSet):
    queryset = models.Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if models.Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    
    def get_queryset(self):
        
        return models.Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer