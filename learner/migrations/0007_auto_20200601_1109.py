# Generated by Django 3.0.3 on 2020-06-01 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0006_auto_20200601_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learning_style',
            name='Active',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='learning_style',
            name='Global',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='learning_style',
            name='Sensitive',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='learning_style',
            name='Visual',
            field=models.IntegerField(default=50),
        ),
    ]
