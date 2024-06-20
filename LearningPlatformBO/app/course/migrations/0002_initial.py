# Generated by Django 5.0.4 on 2024-05-07 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('course', '0001_initial'),
        ('topic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='topics',
            field=models.ManyToManyField(related_name='courses', to='topic.topic'),
        ),
        migrations.AddField(
            model_name='courseadmin',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AddField(
            model_name='courseadmin',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='courseadmin',
            unique_together={('user', 'course')},
        ),
    ]
