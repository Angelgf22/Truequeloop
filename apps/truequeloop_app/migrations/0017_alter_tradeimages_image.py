# Generated by Django 4.2.3 on 2023-10-27 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeloop_app', '0016_remove_openchat_messages_message_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeimages',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='./trades/'),
        ),
    ]
