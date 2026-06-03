from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
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
@api_view()
def collection_list(request):
    collections = models.Collection.objects.all()
    serializer = serializers.CollectionSerializer(collections, many=True)
    return Response(serializer.data)


@api_view()
def collection_detail(request,pk):
    collection = get_object_or_404(models.Collection, pk=pk)
    serializer = serializers.CollectionSerializer(collection)
    return Response(serializer.data)