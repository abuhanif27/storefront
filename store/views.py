from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
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
        return Response('OK')


@api_view()
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    serializer = serializers.ProductSerializer(product,context={'request': request})
    return Response(serializer.data)

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