# Generated by Django 5.0.1 on 2024-01-16 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0003_alter_cart_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart", name="quantity", field=models.SmallIntegerField(),
        ),
    ]