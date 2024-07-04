# Generated by Django 4.2.13 on 2024-06-23 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('version', models.CharField(max_length=50)),
                ('versionSmall', models.IntegerField(default=0)),
                ('versionMiddle', models.IntegerField(default=0)),
                ('versionBig', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SiteBlockVersionList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('version', models.CharField(max_length=50)),
            ],
        ),
    ]
