# Generated by Django 4.2.11 on 2024-05-19 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip4', models.CharField(blank=True, max_length=128)),
                ('ip6', models.CharField(blank=True, max_length=128)),
                ('userName', models.CharField(blank=True, max_length=128)),
                ('country', models.CharField(blank=True, max_length=128)),
                ('city', models.CharField(blank=True, max_length=128)),
                ('loc', models.CharField(blank=True, max_length=128)),
                ('org', models.CharField(blank=True, max_length=128)),
                ('timezone', models.CharField(blank=True, max_length=128)),
                ('hostname', models.CharField(blank=True, max_length=128)),
                ('language', models.CharField(blank=True, max_length=128)),
                ('date', models.CharField(blank=True, max_length=128)),
                ('data', models.CharField(blank=True, max_length=128)),
            ],
        ),
    ]
