# Generated by Django 4.1 on 2023-06-28 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_orderproduct_variation_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='product_prise',
            new_name='product_priсe',
        ),
    ]
