# Generated by Django 3.2 on 2023-07-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_pub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'),
        ),
    ]