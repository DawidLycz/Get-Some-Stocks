# Generated by Django 4.2.5 on 2023-10-22 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('getstocksapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='flag_path',
        ),
        migrations.AlterField(
            model_name='country',
            name='flag_img',
            field=models.CharField(default='BLANKFLAG.png', max_length=200),
        ),
    ]
