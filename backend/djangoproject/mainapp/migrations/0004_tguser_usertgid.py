# Generated by Django 4.2.11 on 2024-05-25 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_tguser'),
    ]

    operations = [
        migrations.AddField(
            model_name='tguser',
            name='userTgId',
            field=models.IntegerField(default=0),
        ),
    ]