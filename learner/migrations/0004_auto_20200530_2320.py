# Generated by Django 3.0.3 on 2020-05-30 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0003_auto_20200526_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='learner',
            name='active',
        ),
        migrations.RemoveField(
            model_name='learner',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='learner',
            name='staff',
        ),
    ]
