# Generated by Django 2.2.3 on 2020-04-04 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_view', '0017_auto_20200404_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]