# Generated by Django 5.0.6 on 2024-05-24 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='raiting',
            field=models.IntegerField(default=0),
        ),
    ]
