# Generated by Django 5.1.6 on 2025-04-02 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alnaser', '0004_product_barcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
