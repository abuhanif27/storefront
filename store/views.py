from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from . import models
from . import serializers

# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = models.Product.objects.select_related('collection').all()
    serializer_class = serializers.ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Product.objects.select_related('collection').all()
    serializer_class = serializers.ProductSerializer
    
    def delete(self, request, pk):
        product = get_object_or_404(models.Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(product)
        return Response(status=status.HTTP_204_NO_CONTENT)




class CollectionList(ListCreateAPIView):
    queryset = models.Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer



class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer
    
    def delete(self, request, pk):
        collection = get_object_or_404(models.Collection, pk=pk)
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.perform_destroy(collection)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    