# Generated by Django 3.0.7 on 2021-07-28 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0015_auto_20200728_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('email', models.CharField(default=None, max_length=30)),
                ('phone', models.CharField(default=None, max_length=20)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address', models.TextField()),
                ('status', models.CharField(default=None, max_length=10)),
                ('transaction_id', models.CharField(default=None, max_length=255)),
                ('currency', models.CharField(default=None, max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
