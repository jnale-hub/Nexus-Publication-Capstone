# Generated by Django 4.2.3 on 2023-07-26 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_games', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameresult',
            name='points',
        ),
    ]
