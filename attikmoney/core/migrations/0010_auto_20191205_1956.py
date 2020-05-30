# Generated by Django 2.2.7 on 2019-12-05 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20191203_2304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emolument',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='asset',
            old_name='id_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='balance',
            old_name='id_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='emolument',
            old_name='id_order',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='id_asset',
            new_name='asset',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='id_broker',
            new_name='broker',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='id_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='id_broker',
            new_name='broker',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='id_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='position',
            old_name='id_user',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='tax',
            old_name='id_user',
            new_name='user',
        ),
    ]
