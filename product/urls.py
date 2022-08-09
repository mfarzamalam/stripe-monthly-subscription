from django.urls import path, include
from .views import *

urlpatterns = [
    path('add/', add_product, name='add_product'),
    path('view/', view_product, name='view_product'),
    path('user/dashboard/', user_dashborad, name='user_dashboard'),
    path('canceled/subscription/<sub_id>/<obj_id>/', CustomerCanceledSubscription.as_view(), name='cancel_subscription'),
]
