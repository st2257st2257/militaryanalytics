# Generated by Django 4.2.13 on 2024-07-01 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='notReadFirst',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chat',
            name='notReadSecond',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='message',
            name='notRead',
            field=models.IntegerField(default=1),
        ),
    ]