# Generated by Django 4.2.5 on 2023-11-07 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0009_market_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='description',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='market',
            name='website',
            field=models.URLField(default='#', null=True),
        ),
    ]
