# Generated by Django 2.2.3 on 2020-04-03 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gamer_view', '0013_remove_category_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]
