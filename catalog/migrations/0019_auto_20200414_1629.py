# Generated by Django 2.1.5 on 2020-04-14 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20200414_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='colors',
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(blank=True, to='catalog.Color', verbose_name='Rengi'),
        ),
    ]