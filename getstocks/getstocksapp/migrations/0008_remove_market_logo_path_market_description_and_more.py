# Generated by Django 4.2.5 on 2023-11-06 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0007_ticker_capitalization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='market',
            name='logo_path',
        ),
        migrations.AddField(
            model_name='market',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterUniqueTogether(
            name='ticker',
            unique_together={('ticker_name', 'origin_market')},
        ),
    ]