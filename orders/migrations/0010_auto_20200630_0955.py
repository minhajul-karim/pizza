# Generated by Django 3.0.7 on 2020-06-30 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200630_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='extra_cheese',
            field=models.CharField(blank=True, default='', max_length=5, null=True),
        ),
    ]
