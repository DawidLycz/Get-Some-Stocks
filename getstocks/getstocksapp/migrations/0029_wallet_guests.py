# Generated by Django 5.0.1 on 2024-01-27 11:18

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0028_walletrecord_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='guests',
            field=models.ManyToManyField(blank=True, related_name='guest_wallets', to=settings.AUTH_USER_MODEL),
        ),
    ]
