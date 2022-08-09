from django.db import models
from django.contrib.auth.models import User
import stripe
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from config.stripe_key import SECRET_KEY

stripe.api_key = SECRET_KEY


# Create your models here.
class UserStripeMapping(models.Model):
    i_user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=256)

    def __str__(self):
        return self.i_user.email


def post_save__create_user_stripe_mapping(sender, instance, created, *args, **kwargs):
    user, created = UserStripeMapping.objects.get_or_create(i_user=instance)
    print("user:", user)
    print("created:", created)
    if user.stripe_id is None or user.stripe_id == '':
        print("inside If:")
        user_stripe_id = stripe.Customer.create(email=instance.email)
        print("user_stripe_id:", user_stripe_id)
        user.stripe_id = user_stripe_id.id
        user.save()


post_save.connect(post_save__create_user_stripe_mapping, sender=User)