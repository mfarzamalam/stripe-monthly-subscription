from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View
from product.models import Product
from stripe_user.models import UserStripeMapping
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
from .models import UserSubscription, ProductStripeMapping

import stripe
from config.settings import DOMAIN_NAME
from config.stripe_key import SECRET_KEY
stripe.api_key = SECRET_KEY



def check_user_is_available_to_subscribe(request, product):
    print("product:", product)
    date_format = "%Y-%m-%d"
    current_date = datetime.datetime.today().strftime(date_format)
    print(current_date)
    user_subscription_obj = UserSubscription.objects.filter(
        i_customer=request.user,
    ).order_by('-subscription_end_date').first()

    print("obj:", user_subscription_obj)
    if user_subscription_obj:
        end_date = user_subscription_obj.subscription_end_date.strftime(date_format)
        print("end_date:", end_date)
        if end_date >= current_date:
            return HttpResponse(f"You already subscribed to <b>{user_subscription_obj.i_product.subscription_type.title()}</b> offer, You cannot subscribe to another")
        else:
            return HttpResponseRedirect(reverse('monthly_subscription', kwargs={'p':int(product)}))
    else:
        return HttpResponseRedirect(reverse('monthly_subscription', kwargs={'p':int(product)}))


class MonthlySubscription(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, p, *args, **kwargs):
        product_id  = p
        quantity = 1

        product_obj = Product.objects.filter(id=product_id).first()
        # subscription_type = product_obj.subscription_type

        product_stripe_mapping_obj = ProductStripeMapping.objects.filter(i_product=product_obj).first()
        stripe_price_id = product_stripe_mapping_obj.product_stripe_price_id

        print("user:", request.user.email)

        user_stripe_mapping_obj = UserStripeMapping.objects.filter(i_user__email=request.user.email).first()
        print("user_stripe_mapping_obj:", user_stripe_mapping_obj)
        stripe_user_id = user_stripe_mapping_obj.stripe_id

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
            success_url=DOMAIN + f"stripe/subscription/create_user_subscription_obj/{{CHECKOUT_SESSION_ID}}/{product_id}",
            cancel_url=DOMAIN + f'single_product/{product_id}',
        )

        return redirect(checkout_session.url, code=303)


def create_user_subscription_obj(request, cs, product):
    sub_id = stripe.checkout.Session.retrieve(cs).get('subscription')
    stripe_obj = stripe.Subscription.retrieve(sub_id)

    date_created = stripe_obj.get('current_period_start')
    date_ended = stripe_obj.get('current_period_end')
    subscription_start_date = datetime.datetime.fromtimestamp(float(date_created))
    subscription_end_date = datetime.datetime.fromtimestamp(float(date_ended))
    
    product = Product.objects.filter(id=product).first()
    
    # subscription_start_date = datetime.fromtimestamp(float(date_created))
    # subscription_end_date = subscription_start_date+relativedelta(months=+1)
    
    print("product:", product)
    print("product__subscription_type:", product.subscription_type)
    print("subscription_start_date:", subscription_start_date)
    print("subscription_end_date:", subscription_end_date)
    
    UserSubscription.objects.create(
        i_customer=request.user, i_product=product, subscription_start_date=subscription_start_date, 
        subscription_end_date=subscription_end_date, subscription_status="active", subscription_id=sub_id
    )

    return HttpResponseRedirect('/')