# Generated by Django 2.2.2 on 2019-11-11 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0009_submission_error'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='exctime',
            field=models.SmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='mem',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
