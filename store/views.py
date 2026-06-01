from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models
from . import serializers

# Create your views here.

@api_view()
def products_list(request):
    products = models.Product.objects.all()
    serializer = serializers.ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)
    serializer = serializers.ProductSerializer(product)
    return Response(serializer.data)