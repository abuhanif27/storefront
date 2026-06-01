from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from . import models

# Create your views here.

@api_view()
def products_list(request):
    return Response("Ok")

@api_view()
def product_detail(request, pk):
    return Response(f"Product with id {pk}")