# Generated by Django 3.0.7 on 2020-06-30 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20200629_1011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='extra_cheese',
            field=models.CharField(default='', max_length=5),
        ),
    ]