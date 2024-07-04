# Generated by Django 4.2.13 on 2024-07-04 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_chat_notreadfirst_chat_notreadsecond_message_notread'),
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
                ('functionNM', models.CharField(blank=True, max_length=128)),
                ('language', models.CharField(blank=True, max_length=128)),
                ('date', models.CharField(blank=True, max_length=128)),
                ('data', models.CharField(blank=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userTgId', models.BigIntegerField(default=0)),
                ('firstNM', models.CharField(blank=True, max_length=128)),
                ('secondNM', models.CharField(blank=True, max_length=128)),
                ('age', models.CharField(blank=True, max_length=128)),
                ('rightData', models.CharField(blank=True, max_length=128)),
            ],
        ),
    ]