# Generated by Django 5.1.2 on 2024-11-13 16:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('totembo', '0014_alter_orderproducts_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproducts',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ordered_products', to='totembo.order', verbose_name='Заказ'),
        ),
    ]
