# Generated by Django 5.0.1 on 2024-01-16 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0002_rename_category_menuitem_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="quantity",
            field=models.SmallIntegerField(default=0),
        ),
    ]
