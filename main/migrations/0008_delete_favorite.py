# Generated by Django 4.0.1 on 2022-01-19 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_remove_favorite_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
