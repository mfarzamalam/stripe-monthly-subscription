from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from product.models import Product
from stripe_user.models import StripeUser
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .models import productSubscription, TwelveMonthSubscription

import stripe
from config.settings import DOMAIN_NAME
from config.stripe_key import SECRET_KEY
stripe.api_key = SECRET_KEY

# Create your views here.


class MonthlySubscription(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, p, q, *args, **kwargs):
        product_id  = p
        quantity = q

        get_product = productSubscription.objects.filter(i_product_id=product_id).first()
        stripe_price_id = get_product.product_stripe_price_id

        print("user:", request.user.email)

        user = StripeUser.objects.filter(i_user__email=request.user.email).first()
        print("user:", user)
        stripe_user_id = user.stripe_id

        # 4242 4242 4242 4242 -- Fake card to test the checkout session
        DOMAIN = DOMAIN_NAME

        checkout_session = stripe.checkout.Session.create(
            customer = stripe_user_id,
            line_items=[
                {
                    'price': stripe_price_id,
                    'quantity': quantity,
                },
            ],
            payment_method_types=['card', 'us_bank_account'],
            mode='subscription',
            success_url=DOMAIN + f"stripe/subscription/create_12_month_subscription/{{CHECKOUT_SESSION_ID}}/{product_id}/",
            cancel_url=DOMAIN + f'single_product/{product_id}',
        )

        return redirect(checkout_session.url, code=303)


def create_12_month_subscription(request, cs, product):
    sub = stripe.checkout.Session.retrieve(cs).get('subscription')
    date_created = stripe.Subscription.retrieve(sub).get('items').get('data')[0].get('created')
    subscription_date = datetime.fromtimestamp(float(date_created))
    product = Product.objects.filter(id=product).first()
    print("subscription_date:", subscription_date)
    date_range = []
    for _ in range(12):
        next_date = subscription_date+relativedelta(months=+1)
        date_range.append(next_date.strftime('%Y-%m-%d'))
        subscription_date = next_date
    print(date_range)

    TwelveMonthSubscription.objects.bulk_create(
        TwelveMonthSubscription(customer=request.user, product=product, month=month, status='unpaid')
        for month in date_range
    )

    return HttpResponseRedirect('/')