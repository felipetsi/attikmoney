# Generated by Django 2.2.7 on 2019-12-04 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20191202_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assettype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
    ]
