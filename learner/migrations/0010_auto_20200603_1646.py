# Generated by Django 3.0.3 on 2020-06-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0009_auto_20200603_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session_log',
            name='Rating',
            field=models.FloatField(default=0),
        ),
    ]
