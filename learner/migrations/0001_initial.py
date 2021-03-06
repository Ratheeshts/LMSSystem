# Generated by Django 3.0.3 on 2020-05-25 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Learner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Age', models.IntegerField(default=18)),
                ('Gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=3, null=True)),
                ('Branch', models.CharField(choices=[('CS', 'Computer Science'), ('MCS', 'Mathematics with Computer Science'), ('BCS', 'BTech Computer Science'), ('BIT', 'BTech Information Technology'), ('MCA', 'Master of Computer Applications')], max_length=50, null=True)),
                ('Qualification', models.CharField(choices=[('HS', 'HS'), ('Post-Graduate', 'Post-Graduate'), ('Graduate', 'Graduate')], max_length=50, null=True)),
                ('BackgroundKnowledge', models.CharField(choices=[('Expert', 'Expert'), ('Basic', 'Basic'), ('Intermediate', 'Intermediate')], default='Basic', max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
