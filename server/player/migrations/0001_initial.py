# Generated by Django 4.2.4 on 2023-09-06 11:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=48, unique=True)),
                ('wins', models.IntegerField(blank=True, default=0)),
                ('losses', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]
