from django.urls import path
from .views import (
    MonthlySubscription,
    create_user_subscription_obj,
    check_user_is_available_to_subscribe
)


urlpatterns = [
    path('user/<int:product>/', check_user_is_available_to_subscribe, 
    name='check_user_is_available_to_subscribe'),
    
    path('Monthly/<int:p>/', MonthlySubscription.as_view(), name='monthly_subscription'),
    
    path('create_user_subscription_obj/<cs>/<product>/', 
    create_user_subscription_obj, name='create_12_month_subscription'),
]
