# Generated by Django 2.2.3 on 2020-04-02 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_view', '0005_remove_user_userid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gamer_view.User'),
        ),
    ]
