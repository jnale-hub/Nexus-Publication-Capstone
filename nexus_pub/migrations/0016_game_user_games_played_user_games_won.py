# Generated by Django 4.2.3 on 2023-07-25 03:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_pub', '0015_user_points_alter_article_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('played_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='played_games', to=settings.AUTH_USER_MODEL)),
                ('won_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='won_games', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='games_played',
            field=models.ManyToManyField(blank=True, related_name='players_played', to='nexus_pub.game'),
        ),
        migrations.AddField(
            model_name='user',
            name='games_won',
            field=models.ManyToManyField(blank=True, related_name='players_won', to='nexus_pub.game'),
        ),
    ]
