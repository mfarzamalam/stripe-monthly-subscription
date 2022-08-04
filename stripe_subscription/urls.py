from django.urls import path
from .views import MonthlySubscription, create_12_month_subscription

urlpatterns = [
    path('Monthly/<int:p>/<int:q>/', MonthlySubscription.as_view(), name='monthly_subscription'),
    path('create_12_month_subscription/<cs>/<product>/', create_12_month_subscription, name='create_12_month_subscription')
]
