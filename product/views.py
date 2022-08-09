from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from stripe_subscription.models import ProductStripeMapping, UserSubscription
from stripe_user.models import UserStripeMapping
from .models import Product
import stripe
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


def home_page(request):
    return render(request, 'product/home.html')


def user_dashborad(request):
    #  cronjob start
    user_stripe_id = UserStripeMapping.objects.filter(i_user=request.user).first().stripe_id
    print("user_stripe_id:", user_stripe_id)
    # stripe_customer_qs = stripe.Customer.retrieve("cus_MBSycfc3VRAkH8")
    # print("stripe_customer_qs:", stripe_customer_qs)
    
    stripe_sub_qs = stripe.Subscription.list(customer=user_stripe_id)
    print("stripe_sub_qs:", len(stripe_sub_qs))

    for stripe_obj in stripe_sub_qs:
        print("stripe_obj:", stripe_obj)
        stripe_obj_id = stripe_obj.id
        user_sub_obj = UserSubscription.objects.filter(subscription_id=stripe_obj_id).first()
        if not user_sub_obj:
            stripe_product_id = stripe_obj.plan.product
            date_created = stripe_obj.get('current_period_start')
            date_ended = stripe_obj.get('current_period_end')
            subscription_start_date = datetime.datetime.fromtimestamp(float(date_created))
            subscription_end_date = datetime.datetime.fromtimestamp(float(date_ended))
            try:
                product_obj = ProductStripeMapping.objects.get(product_stripe_id=stripe_product_id).i_product
            except:
                break
            
            # print("stripe_product_id:", stripe_product_id)
            # print("date_created:", date_created)
            # print("date_ended:", date_ended)
            # print("subscription_start_date:", subscription_start_date)
            # print("subscription_end_date:", subscription_end_date)
            # print("product_obj:", product_obj)
            UserSubscription.objects.create(
                i_customer = request.user,
                i_product = product_obj,
                subscription_start_date = subscription_start_date,
                subscription_end_date = subscription_end_date,
                subscription_status = 'active',
                subscription_id = stripe_obj_id
            )
            print("obj is created")
            print()
    #  cronjob end

    data = UserSubscription.objects.filter(i_customer=request.user)
    context = {'data_dict': data}
    return render(request, 'product/user_dashboard.html', context)


# @login_required
def view_product(request):
    current_date = datetime.datetime.today().strftime("%y-%m-%d")
    print("current_date:", current_date)
    product_qs = list(Product.objects.all().values())
    for product_obj in product_qs:
        product_obj.update({'button': 'buy'})
        print("button:", product_obj.get('button'))

    context = {'products': product_qs}
    return render(request, 'product/view_product.html', context)


def add_product(request):
    if request.method == "POST":
        name = request.POST.get('product_name')
        price = request.POST.get('product_price')
        desc = request.POST.get('product_desc')
        image = request.POST.get('product_image')
        plan = request.POST.get('plan')
        print("name:", name)
        print("price:", price)
        print("desc:", desc)
        print("image:", image)
        print("plan:", plan)

        Product.objects.create(name=name, price=price, description=desc, subscription_type=plan)
        messages.success(request, 'Successfully Added Product.')
        return HttpResponseRedirect("/")
    else:
        if request.method == "GET":
            return render(request, 'product/add_product.html')


class CustomerCanceledSubscription(LoginRequiredMixin, View):
    def get(self, request, sub_id, obj_id, *args, **kwargs):
        stripe.Subscription.delete(sub_id)
        UserSubscription.objects.filter(id=obj_id).update(subscription_status='cancelled')
        return HttpResponseRedirect('/product/user/dashboard/')