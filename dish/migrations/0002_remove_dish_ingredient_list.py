# Generated by Django 4.0.3 on 2022-05-08 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dish', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='ingredient_list',
        ),
    ]
