# Generated by Django 5.1.6 on 2025-04-02 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alnaser', '0006_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
