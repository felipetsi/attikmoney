# Generated by Django 2.2.7 on 2020-03-21 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0046_auto_20200113_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='balance',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='balance',
            name='type_operation',
            field=models.CharField(choices=[('n', 'Normal'), ('d', 'Day trade')], max_length=1, verbose_name='Operation type'),
        ),
    ]
