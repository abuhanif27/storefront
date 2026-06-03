from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from . import models
from . import serializers

# Create your views here.

@api_view(['GET','POST'])
def products_list(request):
    if request.method == 'GET':
        products = models.Product.objects.all()
        serializer = serializers.ProductSerializer(products, many=True,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PATCH','DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    if request.method == 'GET':
        serializer = serializers.ProductSerializer(product,context={'request': request})
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = serializers.ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an order item.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        collections = models.Collection.objects.annotate(products_count=Count('product')).all()
        serializer = serializers.CollectionSerializer(collections, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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