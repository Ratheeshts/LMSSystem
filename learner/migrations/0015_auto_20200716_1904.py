# Generated by Django 3.0.3 on 2020-07-16 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learner', '0014_auto_20200613_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learner',
            name='Learning_Sessions',
            field=models.ManyToManyField(related_name='lnr', to='learner.Learning_Session'),
        ),
        migrations.AlterField(
            model_name='learning_session',
            name='Learning_Session_Logs',
            field=models.ManyToManyField(related_name='l_s', to='learner.Session_Log'),
        ),
        migrations.AlterField(
            model_name='session_log',
            name='VisitedMaterial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slog', to='learner.LearningMaterial'),
        ),
    ]
