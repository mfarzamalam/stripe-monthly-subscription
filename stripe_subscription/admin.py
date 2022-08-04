from django.contrib import admin
from .models import productSubscription, TwelveMonthSubscription

# Register your models here.

admin.site.register(productSubscription)
admin.site.register(TwelveMonthSubscription)