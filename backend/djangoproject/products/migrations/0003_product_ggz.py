# Generated by Django 4.2.13 on 2024-06-23 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_ggz'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ggz',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]