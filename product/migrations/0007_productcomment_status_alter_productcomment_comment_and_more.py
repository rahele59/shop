# Generated by Django 5.1.4 on 2025-01-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_status_alter_productcomment_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcomment',
            name='status',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='productcomment',
            name='rate',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
