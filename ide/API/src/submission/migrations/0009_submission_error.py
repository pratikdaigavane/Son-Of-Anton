# Generated by Django 2.2.2 on 2019-10-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0008_auto_20191024_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='error',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]