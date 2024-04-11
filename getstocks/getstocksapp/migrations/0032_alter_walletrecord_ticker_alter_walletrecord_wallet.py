# Generated by Django 5.0.1 on 2024-03-11 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0031_alter_ticker_origin_market'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletrecord',
            name='ticker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_records', to='getstocksapp.ticker'),
        ),
        migrations.AlterField(
            model_name='walletrecord',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='getstocksapp.wallet'),
        ),
    ]