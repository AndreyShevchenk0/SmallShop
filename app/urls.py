from django.urls import path
from .views import test_view


urlpatterns = [
    path('', test_view, name='base'),
    #path('', views.mod, name='base'),
    #path('myJob/', views.xer, name='myJob'),
    #path('customer/<srt:pk_test>/', views.costomer, name='costomer'),
]
