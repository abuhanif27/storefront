from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products-list'),
    path('products/<int:pk>/',views.ProductDetail.as_view(), name='products-detail'),
    path('collections/',views.collection_list, name='collections-list'), 
    path('collections/<int:pk>/',views.collection_detail, name='collection-detail'),
]