# Generated by Django 4.1 on 2022-08-09 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_subscription', '0006_rename_subscription_end_usersubscription_subscription_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='subscription_id',
            field=models.CharField(default='sub_asdasd213', max_length=256),
            preserve_default=False,
        ),
    ]