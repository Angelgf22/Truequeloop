# Generated by Django 4.2.3 on 2023-09-13 03:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('truequeloop_app', '0004_remove_location_location_trade_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='location_user',
            new_name='location',
        ),
    ]
