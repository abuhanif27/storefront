from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F, Value, Func, Q,Value,ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Min, Max, Avg
from django.db import transaction, connection
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from store.models import Product,Customer,Order,OrderItem,Address
from tags.models import TaggedItem



def say_hello(request):
    with connection.cursor() as cursor:
        queryset = cursor.execute("SELECT * FROM store_collection")
        cursor.callproc("get_customers", [1, 2])
        print(queryset)
    
    return render(request, 'hello.html', {'name': 'Mosh'})