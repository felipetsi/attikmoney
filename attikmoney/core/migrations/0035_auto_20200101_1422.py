# Generated by Django 2.2.7 on 2020-01-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20200101_1355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broker',
            name='name',
            field=models.SlugField(max_length=100, verbose_name='Name'),
        ),
    ]
