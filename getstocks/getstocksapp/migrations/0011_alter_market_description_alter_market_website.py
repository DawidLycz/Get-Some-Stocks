# Generated by Django 4.2.5 on 2023-11-07 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0010_alter_market_description_alter_market_website'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='market',
            name='website',
            field=models.URLField(blank=True, default='#'),
        ),
    ]
