# Generated by Django 4.0.6 on 2023-08-08 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='url',
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.URLField(),
        ),
    ]