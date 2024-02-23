# Generated by Django 4.2.4 on 2024-02-22 22:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teachers', '0025_finalgrade_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('is_visible', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teachers.myclass')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('question_text', models.CharField(max_length=200)),
                ('option1', models.CharField(max_length=100)),
                ('option2', models.CharField(max_length=100)),
                ('option3', models.CharField(max_length=100)),
                ('option4', models.CharField(max_length=100)),
                ('correct_answer', models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.module')),
            ],
        ),
    ]
