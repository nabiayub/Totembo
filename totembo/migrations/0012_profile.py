# Generated by Django 5.1.2 on 2024-11-07 17:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('totembo', '0011_reviews_parent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=50, verbose_name='Номер телефона')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Улица')),
                ('home', models.CharField(blank=True, max_length=50, null=True, verbose_name='Дом №:')),
                ('flat', models.CharField(blank=True, max_length=50, null=True, verbose_name='Квартира №: ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
