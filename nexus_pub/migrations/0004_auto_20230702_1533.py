# Generated by Django 3.2 on 2023-07-02 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nexus_pub', '0003_auto_20230702_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='news',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_category', to='nexus_pub.newscategory'),
        ),
    ]
