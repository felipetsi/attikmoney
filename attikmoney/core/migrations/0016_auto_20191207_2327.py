# Generated by Django 2.2.7 on 2019-12-08 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20191207_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='operation_type',
            field=models.CharField(choices=[('b', 'Buy'), ('s', 'Sale')], max_length=1, verbose_name='Operation type'),
        ),
    ]
