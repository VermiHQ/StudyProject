# Generated by Django 4.0.3 on 2022-05-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0008_alter_dish_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='user_likes',
            field=models.TextField(null=True),
        ),
    ]
