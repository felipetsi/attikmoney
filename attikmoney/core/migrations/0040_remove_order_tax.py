# Generated by Django 2.2.7 on 2020-01-03 01:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20200102_2219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tax',
        ),
    ]