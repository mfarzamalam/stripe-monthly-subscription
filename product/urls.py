from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('view/', view_product, name='view_product'),
]
