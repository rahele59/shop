# Generated by Django 5.1.4 on 2025-01-14 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_category_product_category_delete_productcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status_is_banner',
            field=models.BooleanField(default=False),
        ),
    ]
