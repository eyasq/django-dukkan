# Generated by Django 5.1.6 on 2025-04-02 11:25

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alnaser', '0005_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
