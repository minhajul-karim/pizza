# Generated by Django 3.0.7 on 2020-06-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='extra_cheese',
            field=models.CharField(default='No', max_length=5),
        ),
    ]
