# Generated by Django 2.2.10 on 2020-05-20 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_color_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True),
        ),
    ]