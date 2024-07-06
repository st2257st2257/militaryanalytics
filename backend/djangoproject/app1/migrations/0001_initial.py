# Generated by Django 4.2.13 on 2024-07-06 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024)),
                ('data', models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='EmailForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=1024)),
                ('name', models.CharField(blank=True, max_length=1024)),
                ('email', models.CharField(blank=True, max_length=1024)),
                ('phone', models.CharField(blank=True, max_length=1024)),
                ('company', models.CharField(blank=True, max_length=1024)),
                ('message', models.CharField(blank=True, max_length=1024)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photoLink', models.CharField(blank=True, max_length=255)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('date', models.CharField(blank=True, max_length=1024)),
                ('type', models.IntegerField(default=0)),
                ('userId', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('cover', models.ImageField(upload_to='images/')),
                ('fileData', models.FileField(upload_to='fileData/')),
            ],
        ),
        migrations.CreateModel(
            name='UserFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.CharField(max_length=255)),
                ('user_owner', models.CharField(max_length=255)),
                ('object_type', models.CharField(blank=True, max_length=255)),
                ('file_name', models.CharField(blank=True, max_length=255)),
                ('file_static_url', models.CharField(blank=True, max_length=255)),
                ('file_image', models.ImageField(upload_to='fileImages/')),
                ('file_data', models.FileField(upload_to='fileData/')),
                ('visibility', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstNM', models.CharField(max_length=20)),
                ('secondNM', models.CharField(max_length=20)),
                ('salary', models.IntegerField(default=0)),
                ('salary_old', models.IntegerField(default=0)),
            ],
        ),
    ]
