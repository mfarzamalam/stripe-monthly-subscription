from django.db import models
from product.models import Product
import stripe
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from config.stripe_key import SECRET_KEY
stripe.api_key = SECRET_KEY


# STATUS_CHOICES = (
#     ('active', 'active'),
#     ('unpaid', 'unpaid'),
#     ('cancelled', 'cancelled'),
# )


# class UpComingSubscription(models.Model):
#     customer = models.ForeignKey(User, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     month = models.DateTimeField()
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES)

#     def __str__(self):
#         return str(self.customer)


PRODUCT_INTERVAL = (
    ('month', 'month'),
    ('week', 'week'),
    ('day', 'day'),
)

SUSBSCRIPTION_STATUS = (
    ('active', 'active'),
    ('cancelled', 'cancelled'),
)


class ProductStripeMapping(models.Model):
    i_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_stripe_id = models.CharField(max_length=100, null=True, blank=True)
    product_stripe_price_id = models.CharField(max_length=100, null=True, blank=True)
    product_interval = models.CharField(max_length=10, choices=PRODUCT_INTERVAL, default='month')
    currency = models.CharField(max_length=256, default='USD')

    def __str__(self):
        return self.i_product.name


# run after every product save method call
def post_save_product(sender, instance, created, *args, **kwargs):
    product       = Product.objects.get(pk=instance.pk)
    product_subscription_obj, is_created = ProductStripeMapping.objects.get_or_create(i_product=product)
    product_name  = product.name
    product_price = int(product.price*100)
    product_price_id = product_subscription_obj.product_stripe_price_id
    product_id       = product_subscription_obj.product_stripe_id
    product_interval = product_subscription_obj.product_interval
    currency = product_subscription_obj.currency

    # When new product is created, object of product and price is created.
    if product_subscription_obj.product_stripe_id is None or product_subscription_obj.product_stripe_id == '':
        print("product->if")
        new_product_stripe_id = stripe.Product.create(name=product.name)

        new_product_price_is_subscribe_id = stripe.Price.create(
                                unit_amount=product_price,
                                currency=str(currency),
                                recurring={"interval": str(product_interval)},
                                product=new_product_stripe_id.id,
                            )

        product_subscription_obj.product_stripe_id = new_product_stripe_id.id
        product_subscription_obj.product_stripe_price_id = new_product_price_is_subscribe_id.id
        product_subscription_obj.save()

    # if the product with stripe id is already created, else block run
    else:
        print("product->else")
        get_product_object = stripe.Product.retrieve(product_id)

        get_price_object = stripe.Price.retrieve(product_price_id)
        amount           = get_price_object.unit_amount

        # when price is changed, new object of price is created
        # we cannot update the prvious price as that will not work
        if product_price != amount:
            print("product->else / if -> amount")
            new_price_is_subscribe_id = stripe.Price.create(
                                unit_amount=product_price,
                                currency=str(currency),
                                recurring={"interval": str(product_interval)},
                                product=product_id,
                            )

            product_subscription_obj.product_stripe_price_id = new_price_is_subscribe_id.id
            product_subscription_obj.save()

        # checking if the product name is same or changed, if changed then change this into stripe as well
        if product_name != get_product_object.name:
            print("product->else / if -> name")
            stripe.Product.modify(product_id, name=product_name)



class UserSubscription(models.Model):
    i_customer = models.ForeignKey(User, on_delete=models.CASCADE)
    i_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()
    subscription_status = models.CharField(max_length=10, choices=SUSBSCRIPTION_STATUS)
    subscription_id = models.CharField(max_length=256)
    
    def __str__(self):
        return f"{self.i_customer}, {self.i_product}"


post_save.connect(post_save_product, sender=Product)
