# Generated by Django 4.2.13 on 2024-07-04 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_dronehub_specificationfile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basket',
            name='product',
        ),
        migrations.RemoveField(
            model_name='basket',
            name='user',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Basket',
        ),
    ]
