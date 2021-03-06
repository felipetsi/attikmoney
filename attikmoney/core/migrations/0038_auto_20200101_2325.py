# Generated by Django 2.2.7 on 2020-01-02 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_auto_20200101_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balance',
            name='balance',
            field=models.FloatField(verbose_name='Balance value'),
        ),
        migrations.AlterField(
            model_name='balance',
            name='tax_to_pay',
            field=models.FloatField(verbose_name='Tax to pay'),
        ),
        migrations.AlterField(
            model_name='brokerraterule',
            name='greaterthan',
            field=models.FloatField(blank=True, null=True, verbose_name='Greater than'),
        ),
        migrations.AlterField(
            model_name='brokerraterule',
            name='lessthan',
            field=models.FloatField(blank=True, null=True, verbose_name='Less than'),
        ),
        migrations.AlterField(
            model_name='brokerraterule',
            name='rate',
            field=models.FloatField(verbose_name='Broker rate'),
        ),
        migrations.AlterField(
            model_name='dividendyield',
            name='value',
            field=models.FloatField(verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='emolument',
            name='value',
            field=models.FloatField(verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='position',
            name='value',
            field=models.FloatField(verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='interest_rate',
            field=models.FloatField(verbose_name='Value'),
        ),
        migrations.AlterField(
            model_name='tax',
            name='value',
            field=models.FloatField(verbose_name='Value'),
        ),
    ]
