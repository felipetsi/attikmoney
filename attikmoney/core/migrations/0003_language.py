# Generated by Django 2.2.7 on 2019-11-23 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20191115_1958'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(verbose_name='Name')),
                ('value', models.TextField(verbose_name='Value')),
                ('language', models.CharField(max_length=2, verbose_name='Lang')),
            ],
        ),
    ]
