# Generated by Django 4.0.1 on 2022-01-18 06:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_alter_comment_author_alter_comment_ticket_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.BooleanField(default=True)),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='main.ticket')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
