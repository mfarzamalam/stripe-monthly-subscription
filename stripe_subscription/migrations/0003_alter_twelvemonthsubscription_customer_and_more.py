# Generated by Django 4.1 on 2022-08-04 13:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_alter_product_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("stripe_subscription", "0002_twelvemonthsubscription"),
    ]

    operations = [
        migrations.AlterField(
            model_name="twelvemonthsubscription",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="twelvemonthsubscription",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="product.product"
            ),
        ),
    ]
