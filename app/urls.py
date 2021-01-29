from django.urls import path
from .views import test_view, ProductDetailView


urlpatterns = [
    path('', test_view, name='base'),
    path('products/<str:ct_model>/str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    #path('myJob/', views.xer, name='myJob'),
    #path('customer/<srt:pk_test>/', views.costomer, name='costomer'),
]
