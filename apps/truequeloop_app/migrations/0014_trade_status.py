# Generated by Django 4.2.3 on 2023-09-25 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('truequeloop_app', '0013_remove_trade_trade'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Activo'), ('INACTIVE', 'Inactivo')], default='ACTIVE', max_length=10),
        ),
    ]
