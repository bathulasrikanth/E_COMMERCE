# Generated by Django 5.0.6 on 2024-10-20 04:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("smileapp", "0005_alter_product_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="cart",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="smileapp.cart",
            ),
        ),
    ]
