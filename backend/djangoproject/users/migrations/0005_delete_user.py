# Generated by Django 4.2.13 on 2024-07-05 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_delete_basket'),
        ('users', '0004_user_image_user_walletaddress_user_walletvolume'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
