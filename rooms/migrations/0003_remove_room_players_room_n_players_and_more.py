# Generated by Django 5.0 on 2024-01-22 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='players',
        ),
        migrations.AddField(
            model_name='room',
            name='n_players',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='room',
            name='max_players',
            field=models.PositiveIntegerField(default=7),
        ),
    ]
