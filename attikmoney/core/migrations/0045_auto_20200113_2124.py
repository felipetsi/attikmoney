# Generated by Django 2.2.7 on 2020-01-14 00:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20200113_2122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-updated_at']},
        ),
    ]
