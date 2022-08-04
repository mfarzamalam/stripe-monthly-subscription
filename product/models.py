from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    price = models.IntegerField()
    description = models.TextField(max_length=1024)
    image = models.ImageField(upload_to='product/')

    def __str__(self):
        return self.name