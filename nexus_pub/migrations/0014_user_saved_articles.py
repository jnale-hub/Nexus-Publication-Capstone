# Generated by Django 4.2.3 on 2023-07-10 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_pub', '0013_user_starred_articles_alter_staff_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saved_articles',
            field=models.ManyToManyField(blank=True, related_name='saved_by', to='nexus_pub.article'),
        ),
    ]
