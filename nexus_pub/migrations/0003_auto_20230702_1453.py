# Generated by Django 3.2 on 2023-07-02 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_pub', '0002_auto_20230702_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_author', to='nexus_pub.staff'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='cover',
            field=models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='picture',
            field=models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'),
        ),
    ]
