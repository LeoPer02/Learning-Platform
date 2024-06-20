# Generated by Django 4.1.7 on 2024-02-22 14:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Object creation datetime.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Last updated datetime.')),
                ('is_deleted', models.BooleanField(default=False, help_text='Designates this object as soft deleted.', verbose_name='deleted status')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
