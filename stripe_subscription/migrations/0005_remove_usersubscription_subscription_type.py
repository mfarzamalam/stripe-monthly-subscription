# Generated by Django 4.1 on 2022-08-09 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_subscription', '0004_usersubscription_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersubscription',
            name='subscription_type',
        ),
    ]