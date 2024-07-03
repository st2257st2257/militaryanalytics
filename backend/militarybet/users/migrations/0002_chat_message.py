# Generated by Django 4.2.11 on 2024-05-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstUserLogin', models.CharField(blank=True, max_length=40)),
                ('secondUserLogin', models.CharField(blank=True, max_length=40)),
                ('firstUserName', models.CharField(blank=True, max_length=40)),
                ('secondUserName', models.CharField(blank=True, max_length=40)),
                ('visibility', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=1024)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('chatId', models.IntegerField(default=0)),
                ('ownerLogin', models.CharField(blank=True, max_length=40)),
                ('data', models.FileField(blank=True, upload_to='messages/')),
                ('visibility', models.IntegerField(default=1)),
            ],
        ),
    ]
