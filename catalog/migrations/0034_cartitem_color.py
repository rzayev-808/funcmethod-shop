# Generated by Django 2.2.10 on 2020-06-01 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0033_cart_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='color',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]