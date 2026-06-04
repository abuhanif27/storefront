from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products-list'),
    path('products/<int:pk>/',views.ProductDetail.as_view(), name='products-detail'),
    path('collections/',views.CollectionList.as_view(), name='collections-list'), 
    path('collections/<int:pk>/',views.CollectionDetail.as_view(), name='collection-detail'),
]