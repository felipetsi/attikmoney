# Generated by Django 2.2.7 on 2020-01-13 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_auto_20200113_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(verbose_name='Operation time'),
        ),
    ]
