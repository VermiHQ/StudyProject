# Generated by Django 4.0.3 on 2022-05-08 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0003_alter_dish_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='likes',
            field=models.IntegerField(null=True),
        ),
    ]
