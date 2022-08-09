from django.db import models


SUSBSCRIPTION_TYPE = (
    ('basic', 'basic'),
    ('standard', 'standard'),
    ('enterprise', 'enterprise'),
)


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    price = models.IntegerField()
    description = models.TextField(max_length=1024)
    subscription_type = models.CharField(max_length=10, choices=SUSBSCRIPTION_TYPE)


    def __str__(self):
        return self.name