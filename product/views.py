from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from stripe_subscription.models import UserSubscription
from stripe_user.models import UserStripeMapping
from .models import Product
import stripe
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


def home_page(request):
    return render(request, 'product/home.html')


def user_dashborad(request):
    data = UserSubscription.objects.filter(i_customer=request.user)
    # stripe_user_id = UserStripeMapping.objects.get(i_user=request.user).stripe_id
    # stripe_user_obj = stripe.Subscription.list(customer=stripe_user_id)
    # data = list()
    # for stripe_data in stripe_user_obj:
    #     print(stripe_data)
    #     data.append(
    #         {
    #             'current_period_start': datetime.fromtimestamp(float(stripe_data.current_period_start)),
    #             'current_period_end': datetime.fromtimestamp(float(stripe_data.current_period_end)),
    #         }
    #     )
    #     print()
    context = {'data_dict': data}
    return render(request, 'product/user_dashboard.html', context)


# @login_required
def view_product(request):
    current_date = datetime.datetime.today().strftime("%y-%m-%d")
    print("current_date:", current_date)
    product_qs = list(Product.objects.all().values())
    for product_obj in product_qs:
        # prod_subs = UserProductSubscription.objects.filter(customer=request.user,
        # product_id=product_obj.get('id'), status='active', )
        # if prod_subs:
        #     start_date = prod_subs.subscription_start.strftime('%y-%m-%d')
        #     end_date = prod_subs.subscription_end.strftime('%y-%m-%d')
        #     print("start_date:", start_date)
        #     print("end_date:", end_date)
        #     if start_date <= current_date and end_date >= current_date:
        #         product_obj.update({'button': 'already'})
        #     else:
        #         product_obj.update({'button': 'buy'})
        # else:
        #     product_obj.update({'button': 'buy'})
        product_obj.update({'button': 'buy'})
        
        print("button:", product_obj.get('button'))
        print()

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