# Generated by Django 4.2.5 on 2023-12-29 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0013_ticker_for_display_ticker_full_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='temp_description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
