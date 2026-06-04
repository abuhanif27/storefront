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


class ProductDetail(APIView):
    def get(self, request, pk):
        product = get_object_or_404(models.Product, pk=pk)
        serializer = serializers.ProductSerializer(product,context={'request': request})
        return Response(serializer.data)

    def patch(self, request, pk):
        product = get_object_or_404(models.Product, pk=pk)
        serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)


    def delete(self, request, pk):
        product = get_object_or_404(models.Product, pk=pk)
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        self.product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class CollectionList(ListCreateAPIView):
    queryset = models.Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = serializers.CollectionSerializer


@api_view(['GET','PATCH','DELETE'])
def collection_detail(request,pk):
    collection = get_object_or_404(models.Collection.objects.annotate(products_count=Count('product')), pk=pk)
    if request.method == 'GET':
        serializer = serializers.CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = serializers.CollectionSerializer(collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if collection.product_set.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    