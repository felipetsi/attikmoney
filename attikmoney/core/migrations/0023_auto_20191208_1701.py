# Generated by Django 2.2.7 on 2019-12-08 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_brokerraterule_brokerrateruleassetypebroker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brokerrateruleassetypebroker',
            name='assettype',
        ),
        migrations.RemoveField(
            model_name='brokerrateruleassetypebroker',
            name='broker',
        ),
        migrations.RemoveField(
            model_name='brokerrateruleassetypebroker',
            name='brokerraterule',
        ),
        migrations.RemoveField(
            model_name='brokerrateruleassetypebroker',
            name='user',
        ),
        migrations.DeleteModel(
            name='BrokerRateRule',
        ),
        migrations.DeleteModel(
            name='BrokerRateRuleAsseTypeBroker',
        ),
    ]
