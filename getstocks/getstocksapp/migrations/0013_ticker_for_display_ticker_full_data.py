# Generated by Django 4.2.5 on 2023-11-08 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0012_alter_market_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='for_display',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticker',
            name='full_data',
            field=models.BooleanField(default=False),
        ),
    ]
