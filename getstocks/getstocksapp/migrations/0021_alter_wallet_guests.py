# Generated by Django 5.0.1 on 2024-01-18 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0020_wallet_guests_alter_wallet_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='guests',
            field=models.ManyToManyField(blank=True, related_name='guest_wallets', to=settings.AUTH_USER_MODEL),
        ),
    ]