# Generated by Django 4.0.6 on 2022-08-12 06:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0012_alter_project_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(default=1, related_name='users', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
    ]
