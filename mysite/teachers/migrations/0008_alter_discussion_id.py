# Generated by Django 4.2.4 on 2023-09-20 04:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0007_discussion_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
