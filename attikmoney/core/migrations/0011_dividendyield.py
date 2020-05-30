# Generated by Django 2.2.7 on 2019-12-05 23:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0010_auto_20191205_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='DividendYield',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Value')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Asset')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]