# Generated by Django 2.2.7 on 2020-01-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20200101_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='code',
            field=models.SlugField(max_length=30, verbose_name='Code'),
        ),
    ]
